package com.utp.sidpol.sidpol_backend.service;

import com.utp.sidpol.sidpol_backend.entity.Rol;
import com.utp.sidpol.sidpol_backend.entity.Usuario;
import com.utp.sidpol.sidpol_backend.repository.RolRepository;
import com.utp.sidpol.sidpol_backend.repository.UsuarioRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final RolRepository rolRepository;
    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(RolRepository rolRepository,
                           UsuarioRepository usuarioRepository,
                           PasswordEncoder passwordEncoder) {
        this.rolRepository = rolRepository;
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        Rol rolAdmin = rolRepository.findByNombre("ADMIN")
                .orElseGet(() -> rolRepository.save(new Rol(null, "ADMIN", "Acceso total al sistema")));

        Rol rolUser = rolRepository.findByNombre("USER")
                .orElseGet(() -> rolRepository.save(new Rol(null, "USER", "Acceso limitado a consultas")));

        if (usuarioRepository.findByEmail("admin@sidpol.com").isEmpty()) {
            Usuario admin = new Usuario();
            admin.setNombre("Administrador");
            admin.setEmail("admin@sidpol.com");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setEstado(true);
            admin.setRol(rolAdmin);
            usuarioRepository.save(admin);
        }

        if (usuarioRepository.findByEmail("usuario@sidpol.com").isEmpty()) {
            Usuario user = new Usuario();
            user.setNombre("Usuario Demo");
            user.setEmail("usuario@sidpol.com");
            user.setPassword(passwordEncoder.encode("usuario123"));
            user.setEstado(true);
            user.setRol(rolUser);
            usuarioRepository.save(user);
        }
    }
}