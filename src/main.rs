use macroquad::prelude::*;
use macroquad::ui::{hash, root_ui, widgets};

// Structure to store the user's initial configuration
#[derive(Clone)]
struct BodyConfig {
    mass: f32,
    pos: Vec2,
    vel: Vec2,
    color: Color,
}

// Active Body structure for the simulation
struct Body {
    pos: Vec2,
    vel: Vec2,
    mass: f32,
    color: Color,
    trail: Vec<Vec2>,
}

impl Body {
    fn from_config(config: &BodyConfig) -> Self {
        Self {
            pos: config.pos,
            vel: config.vel,
            mass: config.mass,
            color: config.color,
            trail: Vec::new(),
        }
    }
}

// Function to apply configurations and generate the universe
fn apply_configs(configs: &[BodyConfig]) -> Vec<Body> {
    configs.iter().map(Body::from_config).collect()
}

#[macroquad::main("Dissipative Gravitation Model by Fernando B Couto")]
async fn main() {
    // Initial state editable by the user
    let mut initial_configs = vec![
        BodyConfig { mass: 10.0, pos: vec2(0.0, 150.0), vel: vec2(1.5, 0.0), color: RED },
        BodyConfig { mass: 10.0, pos: vec2(-130.0, -75.0), vel: vec2(-0.75, -1.3), color: GREEN },
        BodyConfig { mass: 10.0, pos: vec2(130.0, -75.0), vel: vec2(-0.75, 1.3), color: BLUE },
    ];

    // Active universe
    let mut bodies = apply_configs(&initial_configs);

    // Global parameters (Thermodynamics and Gravity)
    let mut g_val: f32 = 200.0;
    let mut gamma_val: f32 = 0.5;
    let mut alpha_val: f32 = 1.0;
    let mut is_paused: bool = false;
    
    // Engine stability constants
    let v0: f32 = 0.1;
    let dt: f32 = 0.05;
    let softening: f32 = 5.0;

    loop {
        clear_background(BLACK);

        let center_x = screen_width() / 2.0;
        let center_y = screen_height() / 2.0;

        // --- USER INTERFACE (IMGUI) ---
        widgets::Window::new(hash!(), vec2(20., 20.), vec2(320., 480.))
            .label("Universe Controls")
            .ui(&mut *root_ui(), |ui| {
                
                // Authorship and Title
                ui.label(None, "Dissipative Gravitation Model");
                ui.label(None, "by Fernando B Couto");
                ui.separator();

                ui.label(None, "-- GLOBAL PARAMETERS --");
                ui.slider(hash!(), "Base Gravity (G)", 10.0..1000.0, &mut g_val);
                ui.slider(hash!(), "Space Tension (Gamma)", 0.0..3.0, &mut gamma_val);
                ui.slider(hash!(), "Yield Factor (Alpha)", 0.1..2.0, &mut alpha_val);
                
                ui.separator();
                ui.label(None, "-- INITIAL CONDITIONS --");
                ui.label(None, "Expand to edit:");
                
                // Expandable menus for each body
                widgets::TreeNode::new(hash!(), "Body 1 (Red)")
                    .ui(ui, |ui| {
                        ui.slider(hash!(), "Mass 1", 1.0..200.0, &mut initial_configs[0].mass);
                        ui.slider(hash!(), "Pos X 1", -400.0..400.0, &mut initial_configs[0].pos.x);
                        ui.slider(hash!(), "Pos Y 1", -400.0..400.0, &mut initial_configs[0].pos.y);
                        ui.slider(hash!(), "Vel X 1", -5.0..5.0, &mut initial_configs[0].vel.x);
                        ui.slider(hash!(), "Vel Y 1", -5.0..5.0, &mut initial_configs[0].vel.y);
                    });

                widgets::TreeNode::new(hash!(), "Body 2 (Green)")
                    .ui(ui, |ui| {
                        ui.slider(hash!(), "Mass 2", 1.0..200.0, &mut initial_configs[1].mass);
                        ui.slider(hash!(), "Pos X 2", -400.0..400.0, &mut initial_configs[1].pos.x);
                        ui.slider(hash!(), "Pos Y 2", -400.0..400.0, &mut initial_configs[1].pos.y);
                        ui.slider(hash!(), "Vel X 2", -5.0..5.0, &mut initial_configs[1].vel.x);
                        ui.slider(hash!(), "Vel Y 2", -5.0..5.0, &mut initial_configs[1].vel.y);
                    });

                widgets::TreeNode::new(hash!(), "Body 3 (Blue)")
                    .ui(ui, |ui| {
                        ui.slider(hash!(), "Mass 3", 1.0..200.0, &mut initial_configs[2].mass);
                        ui.slider(hash!(), "Pos X 3", -400.0..400.0, &mut initial_configs[2].pos.x);
                        ui.slider(hash!(), "Pos Y 3", -400.0..400.0, &mut initial_configs[2].pos.y);
                        ui.slider(hash!(), "Vel X 3", -5.0..5.0, &mut initial_configs[2].vel.x);
                        ui.slider(hash!(), "Vel Y 3", -5.0..5.0, &mut initial_configs[2].vel.y);
                    });

                ui.separator();
                
                // Action Buttons
                let pause_label = if is_paused { "Resume" } else { "Pause" };
                if ui.button(None, pause_label) {
                    is_paused = !is_paused;
                }
                
                if ui.button(None, "Apply & Restart") {
                    bodies = apply_configs(&initial_configs);
                    is_paused = false; 
                }
            });

        // --- PHYSICS CALCULATION ---
        if !is_paused {
            let mut forces = vec![Vec2::ZERO; bodies.len()];

            // 1. Gravitational Attraction
            for i in 0..bodies.len() {
                for j in 0..bodies.len() {
                    if i == j { continue; }
                    let dir = bodies[j].pos - bodies[i].pos;
                    let dist_sq = dir.length_squared() + softening * softening; 
                    let force_mag = (g_val * bodies[i].mass * bodies[j].mass) / dist_sq;
                    forces[i] += dir.normalize() * force_mag;
                }
            }

            // 2. Spatial Tension Drag & Integration
            for i in 0..bodies.len() {
                let body = &mut bodies[i];
                let speed = body.vel.length();
                
                // Core formula: Gamma(v) = γ / (v0 + |v|^α)
                let current_gamma = gamma_val / (v0 + speed.powf(alpha_val));
                let drag_force = -body.vel * current_gamma;
                
                let total_force = forces[i] + drag_force;
                let acceleration = total_force / body.mass;

                body.vel += acceleration * dt;
                body.pos += body.vel * dt;

                let current_pos = body.pos;
                body.trail.push(current_pos);
                if body.trail.len() > 800 {
                    body.trail.remove(0);
                }
            }
        }

        // --- RENDERING ---
        
        // Axes / Abstract Barycenter
        draw_line(center_x - 10.0, center_y, center_x + 10.0, center_y, 1.0, DARKGRAY);
        draw_line(center_x, center_y - 10.0, center_x, center_y + 10.0, 1.0, DARKGRAY);

        // 1. Draw "Ghosts" of initial conditions (for setup/aiming)
        for config in &initial_configs {
            let ghost_color = Color::new(config.color.r, config.color.g, config.color.b, 0.4);
            // Ghost position
            draw_circle_lines(config.pos.x + center_x, config.pos.y + center_y, 6.0, 1.5, ghost_color);
            // Velocity Vector (Aiming line)
            draw_line(
                config.pos.x + center_x,
                config.pos.y + center_y,
                config.pos.x + center_x + (config.vel.x * 15.0),
                config.pos.y + center_y + (config.vel.y * 15.0),
                1.5,
                ghost_color
            );
        }

        // 2. Draw Active Universe
        for body in &bodies {
            // Draw trails
            if body.trail.len() > 1 {
                for i in 0..(body.trail.len() - 1) {
                    let p1 = body.trail[i];
                    let p2 = body.trail[i + 1];
                    draw_line(
                        p1.x + center_x, p1.y + center_y,
                        p2.x + center_x, p2.y + center_y,
                        1.5,
                        Color::new(body.color.r, body.color.g, body.color.b, 0.5),
                    );
                }
            }
            // Dynamic body size based on mass
            let radius = 3.0 + (body.mass / 20.0);
            draw_circle(body.pos.x + center_x, body.pos.y + center_y, radius, body.color);
        }

        // Visual pause indicator
        if is_paused {
            draw_text("UNIVERSE PAUSED", center_x - 80.0, screen_height() - 30.0, 22.0, YELLOW);
        }

        next_frame().await
    }
}