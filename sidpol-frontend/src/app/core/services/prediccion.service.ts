import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

export interface PrediccionRequest {
  anio: number;
  mes: number;
  dpto_hecho_new: string;
  es_delito_x: string;
}

export interface PrediccionResponse {
  status: string;
  prediccion_total_delitos: number;
  nivel_alerta: string;
  metadata_tecnica: any;
  mensaje_ejecutivo: string;
}

@Injectable({
  providedIn: 'root'
})
export class PrediccionService {
  private readonly API_URL = 'http://localhost:8080/api/predicciones';

  constructor(private http: HttpClient, private auth: AuthService) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.auth.getToken()}`
    });
  }

  predecir(request: PrediccionRequest): Observable<PrediccionResponse> {
    return this.http.post<PrediccionResponse>(
      `${this.API_URL}/incidencia`,
      request,
      { headers: this.getHeaders() }
    );
  }

  obtenerCatalogos(): Observable<any> {
    return this.http.get(`${this.API_URL}/catalogos`, { headers: this.getHeaders() });
  }

  obtenerMetricas(): Observable<any> {
    return this.http.get(`${this.API_URL}/model/metrics`, { headers: this.getHeaders() });
  }

  obtenerGraficos(): Observable<any> {
    return this.http.get(`${this.API_URL}/model/graficos`, { headers: this.getHeaders() });
  }

  predecirAnual(anio: number, dpto: string, tipo: string): Observable<any> {
    return this.http.get(`${this.API_URL}/incidencia/anual`, {
      headers: this.getHeaders(),
      params: { anio: anio, dpto: dpto, tipo: tipo }
    });
  }

  predecirNacional(anio: number, tipo: string): Observable<any> {
    return this.http.get(`${this.API_URL}/incidencia/nacional`, {
      headers: this.getHeaders(),
      params: { anio: anio, tipo: tipo }
    });
  }

  predecirGeneral(anio: number, dpto?: string, tipo?: string, mes?: number): Observable<any> {
    const body: any = { anio };
    if (dpto) body['dpto_hecho_new'] = dpto;
    if (tipo) body['es_delito_x'] = tipo;
    if (mes !== undefined && mes !== null) body['mes'] = mes;
    return this.http.post(`${this.API_URL}/incidencia/general`, body, {
      headers: this.getHeaders()
    });
  }
}
