use macroquad::prelude::*;
use macroquad::ui::{hash, root_ui, widgets};

// Structure to store the user's initial configuration for a body
#[derive(Clone)]
struct BodyConfig {
    mass: f32,
    pos: Vec2,
    vel: Vec2,
    color: Color,
}

// Active Body structure for the running simulation
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

// Function to apply initial configurations and generate the active universe
fn apply_configs(configs: &[BodyConfig]) -> Vec<Body> {
    configs.iter().map(Body::from_config).collect()
}

// Color palette for dynamically added bodies (using SKYBLUE to avoid compilation errors)
const PALETTE: [Color; 8] = [RED, GREEN, BLUE, YELLOW, MAGENTA, SKYBLUE, ORANGE, PURPLE];

#[macroquad::main("Dissipative Gravitation Model by Fernando B Couto")]
async fn main() {
    // Initial state editable by the user
    let mut initial_configs = vec![
        BodyConfig { mass: 10.0, pos: vec2(0.0, 150.0), vel: vec2(1.5, 0.0), color: PALETTE[0] },
        BodyConfig { mass: 10.0, pos: vec2(-130.0, -75.0), vel: vec2(-0.75, -1.3), color: PALETTE[1] },
        BodyConfig { mass: 10.0, pos: vec2(130.0, -75.0), vel: vec2(-0.75, 1.3), color: PALETTE[2] },
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

    // --- CAMERA VARIABLES (ZOOM AND PAN) ---
    let mut zoom: f32 = 1.0;
    // Initial offset centers the origin (0,0) in the middle of the screen
    let mut pan_offset = vec2(screen_width() / 2.0, screen_height() / 2.0);
    let mut last_mouse_pos = Vec2::from(mouse_position());

    loop {
        clear_background(BLACK);

        let mouse_pos = Vec2::from(mouse_position());

        // --- CAMERA CONTROLS ---
        
        // 1. Panning (Drag with right or middle mouse button)
        if is_mouse_button_down(MouseButton::Right) || is_mouse_button_down(MouseButton::Middle) {
            let delta = mouse_pos - last_mouse_pos;
            pan_offset += delta;
        }

        // 2. Zooming (Mouse Wheel)
        let (_, wheel_y) = mouse_wheel();
        if wheel_y != 0.0 {
            let zoom_factor = 1.1f32;
            let old_zoom = zoom;
            
            if wheel_y > 0.0 { 
                zoom *= zoom_factor; 
            } else { 
                zoom /= zoom_factor; 
            }

            // Math to ensure zooming happens towards the cursor's current position
            pan_offset = mouse_pos - (mouse_pos - pan_offset) * (zoom / old_zoom);
        }
        
        last_mouse_pos = mouse_pos;

        // --- HUD / ON-SCREEN TEXTS ---
        
        // Main Title (Simulated Bold using a +1 pixel offset on the X axis)
        let title = "DISSIPATIVE GRAVITATION MODEL";
        draw_text(title, 20.0, 40.0, 32.0, WHITE);
        draw_text(title, 21.0, 40.0, 32.0, WHITE); 
        
        // Disclaimer / Author
        draw_text("by Fernando B Couto", 20.0, 65.0, 24.0, LIGHTGRAY);

        // Help / Tutorials
        draw_text("COMMAND GUIDE:", 20.0, 120.0, 22.0, YELLOW);
        draw_text("[Mouse Wheel]   Zoom towards the cursor", 20.0, 145.0, 20.0, WHITE);
        draw_text("[Right Click]   Drag to pan the camera", 20.0, 165.0, 20.0, WHITE);
        draw_text("[Right Panel]   Add bodies & adjust parameters", 20.0, 185.0, 20.0, WHITE);

        // --- USER INTERFACE (IMGUI) ---
        
        // Window fixed to the right side of the screen
        let panel_x = screen_width() - 340.0;
        
        widgets::Window::new(hash!(), vec2(panel_x, 20.), vec2(320., 550.))
            .label("Universe Controls")
            .ui(&mut *root_ui(), |ui| {
                
                ui.label(None, "-- GLOBAL PARAMETERS --");
                ui.slider(hash!(), "Base Gravity (G)", 10.0..1000.0, &mut g_val);
                ui.slider(hash!(), "Space Tension (Gamma)", 0.0..3.0, &mut gamma_val);
                ui.slider(hash!(), "Yield Factor (Alpha)", 0.1..2.0, &mut alpha_val);
                
                ui.separator();
                ui.label(None, "-- CAMERA --");
                // Resets the camera to the center of the screen
                if ui.button(None, "Reset Camera Position") {
                    zoom = 1.0;
                    pan_offset = vec2(screen_width() / 2.0, screen_height() / 2.0);
                }

                ui.separator();
                ui.label(None, "-- INITIAL CONDITIONS --");
                
                if ui.button(None, "➕ Add New Body") {
                    let idx = initial_configs.len();
                    initial_configs.push(BodyConfig {
                        mass: 10.0,
                        pos: vec2(0.0, 0.0), // Spawns at the origin
                        vel: vec2(0.0, 0.0),
                        color: PALETTE[idx % PALETTE.len()],
                    });
                }
                if ui.button(None, "➖ Remove Last Body") {
                    if !initial_configs.is_empty() { 
                        initial_configs.pop(); 
                    }
                }

                ui.separator();
                // Dynamic configuration menu for N bodies
                for i in 0..initial_configs.len() {
                    let label = format!("Body {} Configuration", i + 1);
                    widgets::TreeNode::new(hash!("node", i), &label)
                        .ui(ui, |ui| {
                            ui.slider(hash!("mass", i), "Mass", 1.0..200.0, &mut initial_configs[i].mass);
                            ui.slider(hash!("posx", i), "Pos X", -400.0..400.0, &mut initial_configs[i].pos.x);
                            ui.slider(hash!("posy", i), "Pos Y", -400.0..400.0, &mut initial_configs[i].pos.y);
                            ui.slider(hash!("velx", i), "Vel X", -5.0..5.0, &mut initial_configs[i].vel.x);
                            ui.slider(hash!("vely", i), "Vel Y", -5.0..5.0, &mut initial_configs[i].vel.y);
                        });
                }

                ui.separator();
                let pause_label = if is_paused { "▶ Resume Simulation" } else { "⏸ Pause Simulation" };
                if ui.button(None, pause_label) { 
                    is_paused = !is_paused; 
                }
                
                if ui.button(None, "🔄 Apply & Restart") {
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
                // Keep the trail length manageable
                if body.trail.len() > 800 {
                    body.trail.remove(0);
                }
            }
        }

        // --- CLOSURE DECLARATION (FIX FOR E0502) ---
        // Defined here so it doesn't borrow zoom/pan_offset while the UI is rendering
        let to_screen = |world_pos: Vec2| -> Vec2 {
            world_pos * zoom + pan_offset
        };

        // --- RENDERING ---
        
        // Render Barycenter / Origin axes
        let center_screen = to_screen(Vec2::ZERO);
        draw_line(center_screen.x - 10.0, center_screen.y, center_screen.x + 10.0, center_screen.y, 1.0, DARKGRAY);
        draw_line(center_screen.x, center_screen.y - 10.0, center_screen.x, center_screen.y + 10.0, 1.0, DARKGRAY);

        // 1. Draw "Ghosts" of initial conditions (for setup/aiming)
        for config in &initial_configs {
            let ghost_color = Color::new(config.color.r, config.color.g, config.color.b, 0.4);
            let p_screen = to_screen(config.pos);
            let vel_screen = to_screen(config.pos + config.vel * 15.0); 
            
            // Scale the radius with the zoom factor
            draw_circle_lines(p_screen.x, p_screen.y, 6.0 * zoom, 1.5, ghost_color);
            draw_line(p_screen.x, p_screen.y, vel_screen.x, vel_screen.y, 1.5, ghost_color);
        }

        // 2. Draw Active Universe
        for body in &bodies {
            // Draw trails
            if body.trail.len() > 1 {
                for i in 0..(body.trail.len() - 1) {
                    let p1 = to_screen(body.trail[i]);
                    let p2 = to_screen(body.trail[i + 1]);
                    draw_line(p1.x, p1.y, p2.x, p2.y, 1.5, Color::new(body.color.r, body.color.g, body.color.b, 0.5));
                }
            }
            // Dynamic body size based on mass and scaled by zoom
            let radius = (3.0 + (body.mass / 20.0)) * zoom;
            let p_screen = to_screen(body.pos);
            draw_circle(p_screen.x, p_screen.y, radius, body.color);
        }

        // Visual pause indicator
        if is_paused {
            draw_text("UNIVERSE PAUSED", screen_width() / 2.0 - 120.0, screen_height() - 40.0, 32.0, YELLOW);
        }

        next_frame().await
    }
}