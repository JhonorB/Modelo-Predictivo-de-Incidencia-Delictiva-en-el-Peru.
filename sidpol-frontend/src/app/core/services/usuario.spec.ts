// @ts-nocheck
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UsuarioService } from './usuario';

describe('UsuarioService', () => {
  let service: UsuarioService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UsuarioService]
    });

    // Inyectamos el servicio y el controlador de pruebas HTTP
    service = TestBed.inject(UsuarioService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Verificamos que no queden peticiones HTTP colgadas después de cada prueba
    httpMock.verify();
  });

  it('debería crearse correctamente el servicio', () => {
    expect(service).toBeTruthy();
  });

  it('debería realizar una petición POST para registrar un usuario', () => {
    // 1. Preparamos los datos falsos que enviaría el formulario
    const mockUsuarioData = {
      nombre: 'Jhon Ordoñez',
      email: 'jhon@utp.edu.pe',
      password: 'password123',
      rolId: 2
    };

    // 2. Preparamos la respuesta que nos daría el backend si todo sale bien
    const mockRespuestaBackend = {
      id: 1,
      ...mockUsuarioData
    };

    // 3. Ejecutamos el método de tu servicio
    service.registrarUsuario(mockUsuarioData).subscribe((respuesta) => {
      // Verificamos que la respuesta recibida sea igual a la del backend simulado
      expect(respuesta).toEqual(mockRespuestaBackend);
    });

    // 4. Interceptamos la petición HTTP que acaba de disparar el servicio
    const req = httpMock.expectOne('http://localhost:8080/api/usuarios/registrar');

    // 5. Verificamos que la petición haya sido por el método correcto (POST)
    expect(req.request.method).toBe('POST');

    // 6. Verificamos que el body de la petición lleve los datos correctos
    expect(req.request.body).toEqual(mockUsuarioData);

    // 7. Resolvemos la petición enviando la respuesta falsa (esto dispara el subscribe)
    req.flush(mockRespuestaBackend);
  });
});
