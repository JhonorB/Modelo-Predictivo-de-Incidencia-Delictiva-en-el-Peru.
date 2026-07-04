import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  mensaje: string = '';
  error: boolean = false;
  cargando: boolean = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private auth: AuthService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    if (this.auth.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
      return;
    }

    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.cargando = true;
    this.error = false;
    this.mensaje = '';
    this.cdr.detectChanges();

    const { email, password } = this.loginForm.value;

    this.auth.login(email, password).subscribe({
      next: () => {
        this.cargando = false;
        this.cdr.detectChanges();
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.cargando = false;
        this.error = true;
        if (err.status === 401 || err.status === 403) {
           this.mensaje = 'Correo o contraseña incorrectos. Inténtalo de nuevo.';
        } else {
           this.mensaje = 'Error al conectarse con el servidor. Inténtalo de nuevo.';
        }
        this.cdr.detectChanges();
      }
    });
  }
}
