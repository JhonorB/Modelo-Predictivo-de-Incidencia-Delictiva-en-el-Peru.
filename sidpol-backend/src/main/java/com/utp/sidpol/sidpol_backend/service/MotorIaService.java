package com.utp.sidpol.sidpol_backend.service;

import com.utp.sidpol.sidpol_backend.dto.PrediccionRequestDTO;
import com.utp.sidpol.sidpol_backend.dto.PrediccionResponseDTO;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.util.Map;
import java.util.HashMap;

@Service
public class MotorIaService {

    private final RestTemplate restTemplate = new RestTemplate();

    private final String MOTOR_IA_BASE = "http://localhost:8000/api/v1";
    private final String PREDICT_URL = MOTOR_IA_BASE + "/predict/incidencia";
    private final String METRICS_URL = MOTOR_IA_BASE + "/model/metrics";
    private final String GRAFICOS_URL = MOTOR_IA_BASE + "/model/graficos";
    private final String CATALOGOS_URL = MOTOR_IA_BASE + "/catalogos";
    private final String GENERAL_URL = MOTOR_IA_BASE + "/predict/general";
    private final String TENDENCIA_URL = MOTOR_IA_BASE + "/model/tendencia";
    private final String COMPARACION_URL = MOTOR_IA_BASE + "/model/comparacion";

    public PrediccionResponseDTO obtenerPrediccion(PrediccionRequestDTO requestDTO) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<PrediccionRequestDTO> request = new HttpEntity<>(requestDTO, headers);
            ResponseEntity<PrediccionResponseDTO> response = restTemplate.postForEntity(
                    PREDICT_URL, request, PrediccionResponseDTO.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al conectar con el Motor de IA (FastAPI): " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerMetricas() {
        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(METRICS_URL, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al obtener métricas del Motor de IA: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerGraficos() {
        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(GRAFICOS_URL, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al obtener gráficos del Motor de IA: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerCatalogos() {
        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(CATALOGOS_URL, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al obtener catálogos del Motor de IA: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerTendencia(int hasta) {
        try {
            String url = TENDENCIA_URL + "?hasta=" + hasta;
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(url, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al obtener tendencia del Motor de IA: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerComparacion() {
        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(COMPARACION_URL, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al obtener comparación de modelos del Motor de IA: " + e.getMessage());
        }
    }

    // ───────────────────────────────────────────────────────────────
    // ENDPOINT ÚNICO: General (batch predict, 1 sola llamada HTTP)
    // Maneja cualquier combinación: anual/mensual, nacional/depto, todos/tipo
    // ───────────────────────────────────────────────────────────────

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerPrediccionGeneral(int anio, String dpto, String tipo, Integer mes) {
        try {
            Map<String, Object> body = new HashMap<>();
            body.put("anio", anio);
            if (dpto != null && !dpto.isEmpty()) body.put("dpto_hecho_new", dpto);
            if (tipo != null && !tipo.isEmpty()) body.put("es_delito_x", tipo);
            if (mes != null) body.put("mes", mes);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(body, headers);
            ResponseEntity<Map<String, Object>> response = restTemplate.postForEntity(
                    GENERAL_URL, request, (Class<Map<String, Object>>) (Class<?>) Map.class);
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException("Error al conectar con el Motor de IA (General): " + e.getMessage());
        }
    }

    // ───────────────────────────────────────────────────────────────
    // MÉTODOS LEGACY (ahora delegan en General — 1 llamada cada uno)
    // ───────────────────────────────────────────────────────────────

    public Map<String, Object> obtenerPrediccionAnual(int anio, String dpto, String tipo) {
        Map<String, Object> general = obtenerPrediccionGeneral(anio, dpto, tipo, null);
        double total = ((Number) general.getOrDefault("total_general", 0)).doubleValue();
        String nivel = (String) general.getOrDefault("nivel_alerta", "BAJO");
        String mesCritico = (String) general.getOrDefault("mes_mas_critico", "");

        String mensaje = String.format(
            "Proyección anual para %d en %s (%s): %,.0f delitos estimados. Mes crítico: %s. Nivel: %s.",
            anio, dpto, tipo, total, mesCritico, nivel
        );

        return Map.of(
            "anio", anio,
            "departamento", dpto,
            "tipo_delito", tipo,
            "total_delitos", Math.round(total),
            "nivel_alerta", nivel,
            "mes_mas_critico", mesCritico,
            "mensaje_ejecutivo", mensaje
        );
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> obtenerPrediccionNacional(int anio, String tipo) {
        Map<String, Object> general = obtenerPrediccionGeneral(anio, null, tipo, null);
        double total = ((Number) general.getOrDefault("total_general", 0)).doubleValue();
        String dptoMax = (String) general.getOrDefault("departamento_mas_critico", "");
        Map<String, Object> desglose = (Map<String, Object>) general.getOrDefault("desglose_departamentos", Map.of());
        int totalDeptos = desglose.size();

        String mensaje = String.format(
            "Proyección nacional para %d (%s): %,.0f delitos estimados en todo el Perú. " +
            "Departamento más crítico: %s.",
            anio, tipo, total, dptoMax
        );

        return Map.of(
            "anio", anio,
            "tipo_delito", tipo,
            "total_nacional", Math.round(total),
            "departamento_mas_critico", dptoMax,
            "total_departamentos", totalDeptos,
            "mensaje_ejecutivo", mensaje
        );
    }
}
