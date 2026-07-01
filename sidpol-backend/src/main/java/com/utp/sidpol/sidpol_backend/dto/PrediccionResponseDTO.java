package com.utp.sidpol.sidpol_backend.dto;

import java.util.Map;

public class PrediccionResponseDTO {
    private String status;
    private double prediccion_total_delitos;
    private String nivel_alerta;
    private Map<String, Object> metadata_tecnica;
    private String mensaje_ejecutivo;

    public PrediccionResponseDTO() {}

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public double getPrediccion_total_delitos() { return prediccion_total_delitos; }
    public void setPrediccion_total_delitos(double prediccion_total_delitos) { this.prediccion_total_delitos = prediccion_total_delitos; }

    public String getNivel_alerta() { return nivel_alerta; }
    public void setNivel_alerta(String nivel_alerta) { this.nivel_alerta = nivel_alerta; }

    public Map<String, Object> getMetadata_tecnica() { return metadata_tecnica; }
    public void setMetadata_tecnica(Map<String, Object> metadata_tecnica) { this.metadata_tecnica = metadata_tecnica; }

    public String getMensaje_ejecutivo() { return mensaje_ejecutivo; }
    public void setMensaje_ejecutivo(String mensaje_ejecutivo) { this.mensaje_ejecutivo = mensaje_ejecutivo; }
}
