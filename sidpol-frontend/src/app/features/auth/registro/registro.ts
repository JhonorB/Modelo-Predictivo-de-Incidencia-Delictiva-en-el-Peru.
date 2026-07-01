import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { UsuarioService } from '../../../core/services/usuario';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './registro.html',
  styleUrls: ['./registro.scss']
})
export class RegistroComponent implements OnInit {
  registroForm!: FormGroup;
  mensaje: string = '';
  error: boolean = false;

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService
  ) { }

  ngOnInit(): void {
    this.initForm();
  }

  initForm(): void {
    this.registroForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      rolId: [2, Validators.required] // Por defecto un rol común/usuario
    });
  }

  onSubmit(): void {
    if (this.registroForm.invalid) {
      this.registroForm.markAllAsTouched();
      return;
    }

    // 1. Empaquetamos los datos en la estructura exacta que pide Java (Hibernate)
    const formValues = this.registroForm.value;
    const usuarioPayload = {
      nombre: formValues.nombre,
      email: formValues.email,
      password: formValues.password,
      estado: true, // Si tu base de datos exige que no sea nulo
      rol: {
        id: formValues.rolId // <-- Anidamos el ID dentro de un objeto "rol"
      }
    };

    // 2. Enviamos el payload corregido
    this.usuarioService.registrarUsuario(usuarioPayload).subscribe({
      next: (response) => {
        this.error = false;
        this.mensaje = '✅ ¡Usuario registrado exitosamente!';
        this.registroForm.reset({ rolId: 2 });
      },
      error: (err) => {
        this.error = true;
        this.mensaje = '❌ Error al registrar el usuario. Inténtalo de nuevo.';
        console.error(err);
      }
    });
  }
}
