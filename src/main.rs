use macroquad::prelude::*;
use macroquad::ui::{hash, root_ui, widgets};

// Structure to store the user's initial configuration (Now in 3D)
#[derive(Clone)]
struct BodyConfig {
    mass: f32,
    pos: Vec3,
    vel: Vec3,
    color: Color,
}

// Active Body structure for the running simulation (Now in 3D)
struct Body {
    pos: Vec3,
    vel: Vec3,
    mass: f32,
    color: Color,
    trail: Vec<Vec3>,
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

fn apply_configs(configs: &[BodyConfig]) -> Vec<Body> {
    configs.iter().map(Body::from_config).collect()
}

const PALETTE: [Color; 8] = [RED, GREEN, BLUE, YELLOW, MAGENTA, SKYBLUE, ORANGE, PURPLE];

#[macroquad::main("3D Dissipative Gravitation Model by Fernando B Couto")]
async fn main() {
  
    // Pequenos valores em Z adicionados apenas para criar o volume 3D suavemente
    let mut initial_configs = vec![
        BodyConfig { mass: 10.0, pos: vec3(0.0, 150.0, 0.0), vel: vec3(1.5, 0.0, 0.2), color: PALETTE[0] },
        BodyConfig { mass: 10.0, pos: vec3(-130.0, -75.0, 0.0), vel: vec3(-0.75, -1.3, -0.1), color: PALETTE[1] },
        BodyConfig { mass: 10.0, pos: vec3(130.0, -75.0, 0.0), vel: vec3(-0.75, 1.3, 0.1), color: PALETTE[2] },
    ];

    let mut bodies = apply_configs(&initial_configs);

    // Global parameters
    let mut g_val: f32 = 200.0;
    let mut gamma_val: f32 = 0.5;
    let mut alpha_val: f32 = 1.0;
    let mut is_paused: bool = false;
    let mut show_grid: bool = true;
    
    // Engine stability constants
    let v0: f32 = 0.1;
    let dt: f32 = 0.05;
    let softening: f32 = 5.0;

    // --- 3D CAMERA VARIABLES (ORBITAL/ARCBALL) ---
    // alpha = Yaw (Horizontal rotation)
    // beta = Pitch (Vertical rotation)
    let mut cam_alpha: f32 = std::f32::consts::PI / 4.0;
    let mut cam_beta: f32 = std::f32::consts::PI / 6.0;
    let mut cam_radius: f32 = 400.0;
    let mut cam_target = Vec3::ZERO;
    let mut last_mouse_pos = Vec2::from(mouse_position());

    loop {
        clear_background(BLACK);

        let mouse_pos = Vec2::from(mouse_position());

        // --- 3D CAMERA CONTROLS ---
        
        // 1. Orbit (Drag with right mouse button)
        if is_mouse_button_down(MouseButton::Right) {
            let delta = mouse_pos - last_mouse_pos;
            cam_alpha -= delta.x * 0.01;
            cam_beta += delta.y * 0.01;
            
            // Clamp pitch to avoid gimbal lock (flipping upside down)
            let max_beta = std::f32::consts::PI / 2.0 - 0.01;
            cam_beta = cam_beta.clamp(-max_beta, max_beta);
        }

        // 2. Pan Target (Drag with middle mouse button)
        if is_mouse_button_down(MouseButton::Middle) {
            let delta = mouse_pos - last_mouse_pos;
            // Simple panning logic relative to world axes
            cam_target.x -= delta.x * 0.5;
            cam_target.y += delta.y * 0.5;
        }

        // 3. Zoom (Mouse Wheel)
        let (_, wheel_y) = mouse_wheel();
        if wheel_y != 0.0 {
            if wheel_y > 0.0 { cam_radius *= 0.9; } 
            else { cam_radius *= 1.1; }
        }
        
        last_mouse_pos = mouse_pos;

        // Calculate Cartesian Coordinates from Spherical for Camera Position
        let cam_pos = cam_target + vec3(
            cam_radius * cam_beta.cos() * cam_alpha.sin(),
            cam_radius * cam_beta.sin(),
            cam_radius * cam_beta.cos() * cam_alpha.cos(),
        );

        let camera = Camera3D {
            position: cam_pos,
            up: vec3(0., 1., 0.),
            target: cam_target,
            ..Default::default()
        };

        // --- SETUP 3D CONTEXT ---
        set_camera(&camera);

        // Render 3D Grid and Axes
        if show_grid {
            draw_grid(20, 40., LIGHTGRAY, GRAY);
            // World Axes (X=Red, Y=Green, Z=Blue)
            draw_line_3d(Vec3::ZERO, vec3(100.0, 0.0, 0.0), RED);
            draw_line_3d(Vec3::ZERO, vec3(0.0, 100.0, 0.0), GREEN);
            draw_line_3d(Vec3::ZERO, vec3(0.0, 0.0, 100.0), BLUE);
        }

        // --- PHYSICS CALCULATION ---
        if !is_paused {
            let mut forces = vec![Vec3::ZERO; bodies.len()];

            for i in 0..bodies.len() {
                for j in 0..bodies.len() {
                    if i == j { continue; }
                    let dir = bodies[j].pos - bodies[i].pos;
                    let dist_sq = dir.length_squared() + softening * softening; 
                    let force_mag = (g_val * bodies[i].mass * bodies[j].mass) / dist_sq;
                    forces[i] += dir.normalize() * force_mag;
                }
            }

            for i in 0..bodies.len() {
                let body = &mut bodies[i];
                let speed = body.vel.length();
                
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

        // --- 3D RENDERING ---

        // 1. Draw "Ghosts" of initial conditions (for setup/aiming)
        for config in &initial_configs {
            let ghost_color = Color::new(config.color.r, config.color.g, config.color.b, 0.4);
            draw_sphere(config.pos, 3.0, None, ghost_color);
            draw_line_3d(config.pos, config.pos + config.vel * 15.0, ghost_color);
        }

        // 2. Draw Active Universe
        for body in &bodies {
            // Draw 3D trails
            if body.trail.len() > 1 {
                for i in 0..(body.trail.len() - 1) {
                    draw_line_3d(
                        body.trail[i], 
                        body.trail[i + 1], 
                        Color::new(body.color.r, body.color.g, body.color.b, 0.5)
                    );
                }
            }
            // Dynamic body size based on mass
            let radius = 3.0 + (body.mass / 20.0);
            draw_sphere(body.pos, radius, None, body.color);
        }

        // --- SETUP 2D CONTEXT FOR UI ---
        // Crucial step: Return to 2D Screen Space to draw text and ImGui
        set_default_camera();

        // --- HUD / ON-SCREEN TEXTS ---
        let title = "3D DISSIPATIVE GRAVITATION MODEL";
        draw_text(title, 20.0, 40.0, 32.0, WHITE);
        draw_text(title, 21.0, 40.0, 32.0, WHITE); 
        draw_text("by Fernando B Couto", 20.0, 65.0, 24.0, LIGHTGRAY);

        draw_text("3D COMMAND GUIDE:", 20.0, 120.0, 22.0, YELLOW);
        draw_text("[Right Click]   Orbit Camera (Rotate)", 20.0, 145.0, 20.0, WHITE);
        draw_text("[Middle Click]  Pan Camera Target", 20.0, 165.0, 20.0, WHITE);
        draw_text("[Mouse Wheel]   Zoom In/Out", 20.0, 185.0, 20.0, WHITE);

        if is_paused {
            draw_text("UNIVERSE PAUSED", screen_width() / 2.0 - 120.0, screen_height() - 40.0, 32.0, YELLOW);
        }

        // --- USER INTERFACE (IMGUI) ---
        let panel_x = screen_width() - 340.0;
        
        widgets::Window::new(hash!(), vec2(panel_x, 20.), vec2(320., 550.))
            .label("Universe Controls")
            .ui(&mut *root_ui(), |ui| {
                
                ui.label(None, "-- GLOBAL PARAMETERS --");
                ui.slider(hash!(), "Base Gravity (G)", 10.0..1000.0, &mut g_val);
                ui.slider(hash!(), "Space Tension (Gamma)", 0.0..3.0, &mut gamma_val);
                ui.slider(hash!(), "Yield Factor (Alpha)", 0.1..2.0, &mut alpha_val);
                
                ui.separator();
                ui.label(None, "-- CAMERA & VIEW --");
                ui.checkbox(hash!(), "Show Grid & Axes", &mut show_grid);
                if ui.button(None, "Reset Camera Position") {
                    cam_alpha = std::f32::consts::PI / 4.0;
                    cam_beta = std::f32::consts::PI / 6.0;
                    cam_radius = 400.0;
                    cam_target = Vec3::ZERO;
                }

                ui.separator();
                ui.label(None, "-- INITIAL CONDITIONS --");
                
                if ui.button(None, "➕ Add New Body") {
                    let idx = initial_configs.len();
                    initial_configs.push(BodyConfig {
                        mass: 10.0,
                        pos: Vec3::ZERO,
                        vel: Vec3::ZERO,
                        color: PALETTE[idx % PALETTE.len()],
                    });
                }
                if ui.button(None, "➖ Remove Last Body") {
                    if !initial_configs.is_empty() { initial_configs.pop(); }
                }

                ui.separator();
                for i in 0..initial_configs.len() {
                    let label = format!("Body {} Configuration", i + 1);
                    widgets::TreeNode::new(hash!("node", i), &label)
                        .ui(ui, |ui| {
                            ui.slider(hash!("mass", i), "Mass", 1.0..200.0, &mut initial_configs[i].mass);
                            // Now with Z axis for both Position and Velocity
                            ui.slider(hash!("posx", i), "Pos X", -400.0..400.0, &mut initial_configs[i].pos.x);
                            ui.slider(hash!("posy", i), "Pos Y", -400.0..400.0, &mut initial_configs[i].pos.y);
                            ui.slider(hash!("posz", i), "Pos Z", -400.0..400.0, &mut initial_configs[i].pos.z);
                            ui.separator();
                            ui.slider(hash!("velx", i), "Vel X", -5.0..5.0, &mut initial_configs[i].vel.x);
                            ui.slider(hash!("vely", i), "Vel Y", -5.0..5.0, &mut initial_configs[i].vel.y);
                            ui.slider(hash!("velz", i), "Vel Z", -5.0..5.0, &mut initial_configs[i].vel.z);
                        });
                }

                ui.separator();
                let pause_label = if is_paused { "▶ Resume Simulation" } else { "⏸ Pause Simulation" };
                if ui.button(None, pause_label) { is_paused = !is_paused; }
                
                if ui.button(None, "🔄 Apply & Restart") {
                    bodies = apply_configs(&initial_configs);
                    is_paused = false; 
                }
            });

        next_frame().await
    }
}