package com.utp.sidpol.sidpol_backend.repository;

import com.utp.sidpol.sidpol_backend.entity.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    
    // Método vital para el Login: Busca al usuario en MySQL usando su correo electrónico
    Optional<Usuario> findByEmail(String email);
    
    // Método para comprobar si un correo ya está registrado en el sistema
    Boolean existsByEmail(String email);
}