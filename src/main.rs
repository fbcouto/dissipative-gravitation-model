use macroquad::prelude::*;

#[derive(Clone)]
struct BodyConfig {
    mass: f32,
    pos: Vec3,
    vel: Vec3,
    color: Color,
}

struct Body {
    mass: f32,
    pos: Vec3,
    vel: Vec3,
    color: Color,
    trail: Vec<Vec3>,
}

impl Body {
    fn from_config(config: &BodyConfig) -> Self {
        Self {
            mass: config.mass,
            pos: config.pos,
            vel: config.vel,
            color: config.color,
            trail: Vec::new(),
        }
    }
}

const PALETTE: [Color; 8] = [RED, GREEN, BLUE, YELLOW, MAGENTA, SKYBLUE, ORANGE, PURPLE];

#[macroquad::main("3D Dissipative Gravitation Model by Fernando B Couto")]
async fn main() {
    // Configurações iniciais dos corpos (fantasmas de setup)
    let configs = vec![
        BodyConfig { mass: 10.0, pos: vec3(0.0, 150.0, 0.0), vel: vec3(1.5, 0.0, 0.2), color: PALETTE[0] },
        BodyConfig { mass: 10.0, pos: vec3(-130.0, -75.0, 0.0), vel: vec3(-0.75, -1.3, -0.1), color: PALETTE[1] },
        BodyConfig { mass: 10.0, pos: vec3(130.0, -75.0, 0.0), vel: vec3(-0.75, 1.3, 0.1), color: PALETTE[2] },
    ];

    let mut bodies: Vec<Body> = configs.iter().map(Body::from_config).collect();

    // Constantes do Modelo DGM
    let g_val = 200.0;
    let gamma_val = 0.5;   // Tensão Espacial / Coeficiente de Arrasto
    let alpha_val = 1.0;   // Fator de fluidez (Yield Factor)
    let v0 = 0.1;          // Constante de estabilidade do motor
    let dt = 0.05;         // Delta de tempo
    let softening = 5.0;   // Suavização gravitacional para evitar colapsos singulares
    
    let is_paused = false;
    let show_grid = true;

    // Controles da Câmera Arcball
    let mut cam_alpha = std::f32::consts::PI / 4.0;
    let mut cam_beta = std::f32::consts::PI / 6.0;
    let mut cam_radius = 400.0;
    let cam_target = vec3(0.0, 0.0, 0.0);

    loop {
        // --- 1. CONTROLES DE CÂMERA E MOUSE ---
        if is_mouse_button_down(MouseButton::Right) {
            let delta = mouse_delta_position();
            cam_alpha -= delta.x * 2.0;
            cam_beta += delta.y * 2.0;
            
            // Trava de pólos para evitar Gimbal Lock
            let limit = std::f32::consts::PI / 2.0 - 0.01;
            cam_beta = cam_beta.clamp(-limit, limit);
        }
        
        let wheel = mouse_wheel().1;
        if wheel > 0.0 { cam_radius *= 0.9; }
        if wheel < 0.0 { cam_radius *= 1.1; }

        let cam_pos = vec3(
            cam_target.x + cam_radius * cam_beta.cos() * cam_alpha.sin(),
            cam_target.y + cam_radius * cam_beta.sin(),
            cam_target.z + cam_radius * cam_beta.cos() * cam_alpha.cos()
        );

        let camera = Camera3D {
            position: cam_pos,
            target: cam_target,
            up: vec3(0.0, 1.0, 0.0),
           ..Default::default()
        };

        // --- 2. MOTOR FÍSICO DGM (N-BODY) ---
        if!is_paused {
            let mut forces = vec![vec3(0.0, 0.0, 0.0); bodies.len()];
            
            // Cálculo das Forças de Atração e Arrasto Viscoelástico
            for i in 0..bodies.len() {
                for j in 0..bodies.len() {
                    if i == j { continue; }
                    let r_vec = bodies[j].pos - bodies[i].pos;
                    let r_mag = r_vec.length();
                    
                    // Gravitação Suavizada
                    let f_g = (g_val * bodies[i].mass * bodies[j].mass) / (r_mag * r_mag + softening * softening);
                    forces[i] += r_vec.normalize() * f_g;
                }
                
                // Cálculo da Força de Arrasto Inelástico (Dinâmica Pseudo-Plástica)
                let v_mag = bodies[i].vel.length();
                let f_drag = -bodies[i].vel * (gamma_val / (v0 + v_mag.powf(alpha_val)));
                forces[i] += f_drag;
            }

            for i in 0..bodies.len() {
                let a = forces[i] / bodies[i].mass;
                
                // Isolamos a referência mutável para satisfazer o borrow checker
                let body = &mut bodies[i];
                
                // Euler-Cromer: Atualiza-se a VELOCIDADE primeiro...
                body.vel += a * dt; 
                //... e usa-se a nova velocidade para atualizar a POSIÇÃO
                body.pos += body.vel * dt; 

                // Copiamos o valor de posição para evitar um duplo empréstimo na mesma linha
                let current_pos = body.pos;
                
                // Atualização dos rastros orbitais (limite de 800 pontos na memória)
                body.trail.push(current_pos);
                if body.trail.len() > 800 {
                    body.trail.remove(0);
                }
            }
        }

        // --- 3. RENDERIZAÇÃO 3D ---
        set_camera(&camera);
        clear_background(BLACK);

        if show_grid {
            // Correção: adicionado o quarto argumento de cor (ex: DARKGRAY e GRAY)
            draw_grid(20, 10.0, DARKGRAY, GRAY);
            
            // Correção: removido o argumento de espessura (2.0)
            draw_line_3d(vec3(0.0, 0.0, 0.0), vec3(100.0, 0.0, 0.0), RED);
            draw_line_3d(vec3(0.0, 0.0, 0.0), vec3(0.0, 100.0, 0.0), GREEN);
            draw_line_3d(vec3(0.0, 0.0, 0.0), vec3(0.0, 0.0, 100.0), BLUE);
        }

        // Desenhar Corpos Ativos e Rastros
        for body in &bodies {
            // Desenhar rastro contínuo
            if body.trail.len() > 1 {
                for i in 0..(body.trail.len() - 1) {
                    // Correção: removido o argumento de espessura (1.0)
                    draw_line_3d(body.trail[i], body.trail[i+1], body.color);
                }
            }
            // O raio de renderização é escalonado dinamicamente usando a massa 
            let radius = 3.0 + body.mass / 20.0;
            draw_sphere(body.pos, radius, None, body.color);
        }

        // --- 4. RENDERIZAÇÃO 2D (HUD & ImGui) ---
        set_default_camera();
        draw_text("Simulador DGM (Euler-Cromer Activo)", 20.0, 30.0, 20.0, WHITE);
        
        if is_paused {
            draw_text("UNIVERSE PAUSED", screen_width() / 2.0 - 100.0, 50.0, 30.0, RED);
        }

        next_frame().await;
    }
}