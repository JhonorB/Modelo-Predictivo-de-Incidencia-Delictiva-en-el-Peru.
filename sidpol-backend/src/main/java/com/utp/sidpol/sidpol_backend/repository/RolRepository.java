package com.utp.sidpol.sidpol_backend.repository;

import com.utp.sidpol.sidpol_backend.entity.Rol;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RolRepository extends JpaRepository<Rol, Long> {
    // Método para buscar el rol por su nombre (ADMIN o USER)
    Optional<Rol> findByNombre(String nombre);
}