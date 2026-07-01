import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  // Ajusta la URL según los endpoints de tu Spring Boot
// En tu archivo usuario.ts de Angular:
private apiUrl = 'http://localhost:8080/api/usuarios/registrar';

  constructor(private http: HttpClient) { }

  registrarUsuario(usuarioData: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, usuarioData);
  }
}
