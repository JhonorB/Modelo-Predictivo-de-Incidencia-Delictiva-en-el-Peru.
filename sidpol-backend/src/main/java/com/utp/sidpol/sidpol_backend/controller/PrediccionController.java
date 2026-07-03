package com.utp.sidpol.sidpol_backend.controller;

import com.utp.sidpol.sidpol_backend.dto.PrediccionRequestDTO;
import com.utp.sidpol.sidpol_backend.dto.PrediccionResponseDTO;
import com.utp.sidpol.sidpol_backend.service.MotorIaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/predicciones")
@CrossOrigin(origins = "http://localhost:4200")
public class PrediccionController {

    @Autowired
    private MotorIaService motorIaService;

    @PostMapping("/incidencia")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<PrediccionResponseDTO> predecirIncidencia(@RequestBody PrediccionRequestDTO request) {
        PrediccionResponseDTO response = motorIaService.obtenerPrediccion(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/catalogos")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> obtenerCatalogos() {
        Map<String, Object> catalogos = motorIaService.obtenerCatalogos();
        return ResponseEntity.ok(catalogos);
    }

    @GetMapping("/model/metrics")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Object>> obtenerMetricasModelo() {
        Map<String, Object> metricas = motorIaService.obtenerMetricas();
        return ResponseEntity.ok(metricas);
    }

    @GetMapping("/model/graficos")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> obtenerGraficosModelo() {
        Map<String, Object> graficos = motorIaService.obtenerGraficos();
        return ResponseEntity.ok(graficos);
    }

    @GetMapping("/model/tendencia")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> obtenerTendencia(@RequestParam int hasta) {
        Map<String, Object> result = motorIaService.obtenerTendencia(hasta);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/model/comparacion")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Object>> obtenerComparacion() {
        Map<String, Object> result = motorIaService.obtenerComparacion();
        return ResponseEntity.ok(result);
    }

    @GetMapping("/incidencia/anual")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> predecirAnual(
            @RequestParam int anio,
            @RequestParam String dpto,
            @RequestParam String tipo,
            @RequestParam(required = false) Integer mes) {
        if (mes != null) {
            Map<String, Object> result = motorIaService.obtenerPrediccionGeneral(anio, dpto, tipo, mes);
            return ResponseEntity.ok(result);
        }
        Map<String, Object> result = motorIaService.obtenerPrediccionAnual(anio, dpto, tipo);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/incidencia/nacional")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> predecirNacional(
            @RequestParam int anio,
            @RequestParam String tipo,
            @RequestParam(required = false) Integer mes) {
        if (mes != null) {
            Map<String, Object> result = motorIaService.obtenerPrediccionGeneral(anio, null, tipo, mes);
            return ResponseEntity.ok(result);
        }
        Map<String, Object> result = motorIaService.obtenerPrediccionNacional(anio, tipo);
        return ResponseEntity.ok(result);
    }

    @PostMapping("/incidencia/general")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Map<String, Object>> predecirGeneral(@RequestBody Map<String, Object> params) {
        int anio = Integer.parseInt(params.getOrDefault("anio", String.valueOf(java.time.Year.now().getValue())).toString());
        String dpto = params.containsKey("dpto_hecho_new") ? params.get("dpto_hecho_new").toString() : null;
        String tipo = params.containsKey("es_delito_x") ? params.get("es_delito_x").toString() : null;
        Integer mes = params.containsKey("mes") ? Integer.parseInt(params.get("mes").toString()) : null;
        Map<String, Object> result = motorIaService.obtenerPrediccionGeneral(anio, dpto, tipo, mes);
        return ResponseEntity.ok(result);
    }
}
