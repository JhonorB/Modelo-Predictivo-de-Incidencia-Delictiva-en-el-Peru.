package com.utp.sidpol.sidpol_backend.service;

import com.utp.sidpol.sidpol_backend.entity.Usuario;
import com.utp.sidpol.sidpol_backend.repository.UsuarioRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    // Inyección de dependencias (Spring lo hace por ti)
    public UsuarioService(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    // ¡Aquí está tu "guardar_data"!
    public Usuario registrarUsuario(Usuario usuario) {
        // Encriptamos la contraseña antes de guardarla
        usuario.setPassword(passwordEncoder.encode(usuario.getPassword()));
        // Guardamos en la base de datos (Docker)
        return usuarioRepository.save(usuario);
    }
}