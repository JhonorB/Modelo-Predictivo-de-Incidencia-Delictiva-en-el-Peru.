// @ts-nocheck
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';
import { RegistroComponent } from './registro';
import { UsuarioService } from '../../../core/services/usuario';

describe('RegistroComponent', () => {
  let component: RegistroComponent;
  let fixture: ComponentFixture<RegistroComponent>;
  let usuarioServiceSpy: jasmine.SpyObj<UsuarioService>;

  beforeEach(async () => {
    // 1. Creamos un "espía" del servicio para no pegarle al backend real de Spring Boot
    const spy = jasmine.createSpyObj('UsuarioService', ['registrarUsuario']);

    await TestBed.configureTestingModule({
      // Importamos el componente Standalone y el módulo de formularios
      imports: [RegistroComponent, ReactiveFormsModule],
      // Reemplazamos el servicio real por nuestro espía
      providers: [
        { provide: UsuarioService, useValue: spy }
      ]
    }).compileComponents();

    usuarioServiceSpy = TestBed.inject(UsuarioService) as jasmine.SpyObj<UsuarioService>;
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegistroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Esto dispara el ngOnInit()
  });

  it('debería crear el componente correctamente', () => {
    expect(component).toBeTruthy();
  });

  it('debería inicializar el formulario como inválido y con el rol 2 por defecto', () => {
    expect(component.registroForm.valid).toBeFalse();
    expect(component.registroForm.get('rolId')?.value).toBe(2);
  });

  it('debería validar correctamente el formato del correo electrónico', () => {
    const emailControl = component.registroForm.get('email');

    emailControl?.setValue('correo-falso-sin-arroba');
    expect(emailControl?.valid).toBeFalse();

    emailControl?.setValue('test@utp.edu.pe');
    expect(emailControl?.valid).toBeTrue();
  });

  it('debería llamar al servicio y mostrar mensaje de ÉXITO si el formulario es válido', () => {
    // Simulamos que Spring Boot responde con un 200 OK
    usuarioServiceSpy.registrarUsuario.and.returnValue(of({ id: 1, nombre: 'Jhon' }));

    // Llenamos el formulario con datos válidos
    component.registroForm.controls['nombre'].setValue('Jhon Ordoñez');
    component.registroForm.controls['email'].setValue('jhon@utp.edu.pe');
    component.registroForm.controls['password'].setValue('123456');

    // Disparamos la función del botón
    component.onSubmit();

    expect(usuarioServiceSpy.registrarUsuario).toHaveBeenCalled();
    expect(component.error).toBeFalse();
    expect(component.mensaje).toContain('exitosamente');
  });

  it('debería mostrar mensaje de ERROR si el backend falla (ej. correo duplicado)', () => {
    // Simulamos que Spring Boot lanza un error 500 o 400
    usuarioServiceSpy.registrarUsuario.and.returnValue(throwError(() => new Error('Error de red')));

    // Llenamos el formulario con datos válidos
    component.registroForm.controls['nombre'].setValue('Jhon Ordoñez');
    component.registroForm.controls['email'].setValue('jhon@utp.edu.pe');
    component.registroForm.controls['password'].setValue('123456');

    component.onSubmit();

    expect(usuarioServiceSpy.registrarUsuario).toHaveBeenCalled();
    expect(component.error).toBeTrue();
    expect(component.mensaje).toContain('Error al registrar');
  });
});
