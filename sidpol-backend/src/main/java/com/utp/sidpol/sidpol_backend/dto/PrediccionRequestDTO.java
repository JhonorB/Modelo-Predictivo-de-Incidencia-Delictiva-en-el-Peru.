package com.utp.sidpol.sidpol_backend.dto;

public class PrediccionRequestDTO {
    private int anio;
    private int mes;
    private String dpto_hecho_new;
    private String es_delito_x;

    public PrediccionRequestDTO() {}

    public int getAnio() { return anio; }
    public void setAnio(int anio) { this.anio = anio; }

    public int getMes() { return mes; }
    public void setMes(int mes) { this.mes = mes; }

    public String getDpto_hecho_new() { return dpto_hecho_new; }
    public void setDpto_hecho_new(String dpto_hecho_new) { this.dpto_hecho_new = dpto_hecho_new; }

    public String getEs_delito_x() { return es_delito_x; }
    public void setEs_delito_x(String es_delito_x) { this.es_delito_x = es_delito_x; }
}
