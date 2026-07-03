import { Component, OnInit, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { PrediccionService } from '../../core/services/prediccion.service';

import Plotly from 'plotly.js-dist';

const TODO_EL_PERU = 'TODO_EL_PERU';
const TODOS = 'TODOS';
const ANUAL = 'ANUAL';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {
  @ViewChild('graficoPrediccion') graficoPrediccion!: ElementRef;
  @ViewChild('graficoDepartamentos') graficoDepartamentos!: ElementRef;
  @ViewChild('graficoDelitos') graficoDelitos!: ElementRef;
  @ViewChild('graficoTendencia') graficoTendencia!: ElementRef;

  selectedSection: string = 'dashboard';

  anioActual = new Date().getFullYear();
  anioOptions: number[] = Array.from({ length: 2036 - 2018 }, (_, i) => 2018 + i);
  tendenciaOptions: number[] = Array.from({ length: 2036 - 2026 }, (_, i) => 2026 + i);
  tendenciaHasta: number = 2028;
  mesesOptions = [1,2,3,4,5,6,7,8,9,10,11,12];
  mesesNombres = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                  'Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre'];

  getNombreMes(num: number): string {
    return this.mesesNombres[num - 1] || '';
  }

  filtro = {
    anio: this.anioActual,
    periodo: ANUAL,
    dpto_hecho_new: TODO_EL_PERU,
    es_delito_x: TODOS
  };

  cargando = false;
  prediccion: any = null;
  metricas: any = null;
  graficos: any = null;
  catalogos: any = null;
  comparacion: any = null;
  esAdmin = false;
  nombreUsuario = '';

  alertaClase = '';
  fechaActual = new Date();

  config = {
    profileImage: '',
    roleIcon: '🦊',
    userRoleIcon: '🐱',
    themeColor: '#2563eb',
    sidebarCompact: false,
    notificaciones: true,
    sonidoAlerta: false
  };

  availableAdminIcons = ['🦊', '🐺', '🦁', '🐉', '🦅', '🐯'];
  availableUserIcons = ['🐱', '🐶', '🐼', '🐨', '🦊', '🐰'];

  readonly TODO_EL_PERU = TODO_EL_PERU;
  readonly TODOS = TODOS;
  readonly ANUAL = ANUAL;

  constructor(
    public auth: AuthService,
    private predService: PrediccionService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    this.esAdmin = this.auth.isAdmin();
    this.nombreUsuario = this.auth.getNombre() || '';

    this.cargarCatalogos();
    this.cargarGraficos();
    this.cargarConfig();

    if (this.esAdmin) {
      this.cargarMetricas();
      this.cargarComparacion();
    }

    setTimeout(() => this.ejecutarPrediccion(), 800);
  }

  ngAfterViewInit(): void {}

  cargarConfig(): void {
    const saved = localStorage.getItem('sidpol_config');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        this.config = { ...this.config, ...parsed };
      } catch {}
    }
  }

  guardarConfig(): void {
    localStorage.setItem('sidpol_config', JSON.stringify(this.config));
  }

  onProfileImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input?.files?.[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.config.profileImage = e.target?.result as string;
        this.guardarConfig();
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  resetProfileImage(): void {
    this.config.profileImage = '';
    this.guardarConfig();
  }

  selectSection(section: string): void {
    this.selectedSection = section;
    setTimeout(() => this.renderizarGraficosPlotly(), 300);
    if (section === 'dashboard') {
      setTimeout(() => this.cargarTendenciaDinamica(), 300);
    }
    if (section === 'predicciones') {
      setTimeout(() => this.renderizarPrediccion(this.prediccion), 300);
    }
  }

  get pageTitle(): string {
    const titles: Record<string, string> = {
      'dashboard': 'Panel de Control',
      'predicciones': 'Motor de Predicciones',
      'configuracion': 'Configuración del Sistema'
    };
    return titles[this.selectedSection] || 'Panel de Control';
  }

  get pageIcon(): string {
    const icons: Record<string, string> = {
      'dashboard': '📊',
      'predicciones': '🔮',
      'configuracion': '⚙️'
    };
    return icons[this.selectedSection] || '📊';
  }

  cargarCatalogos(): void {
    this.predService.obtenerCatalogos().subscribe({
      next: (data) => { this.catalogos = data; },
      error: () => {}
    });
  }

  cargarMetricas(): void {
    this.predService.obtenerMetricas().subscribe({
      next: (data) => { this.metricas = data; },
      error: () => {}
    });
  }

  cargarComparacion(): void {
    this.predService.obtenerComparacion().subscribe({
      next: (data) => { this.comparacion = data; },
      error: () => {}
    });
  }

  cargarGraficos(): void {
    this.predService.obtenerGraficos().subscribe({
      next: (data) => {
        this.graficos = data;
        this.renderizarGraficosPlotly();
      },
      error: () => {}
    });
  }

  cargarTendenciaDinamica(): void {
    this.predService.obtenerTendencia(this.tendenciaHasta).subscribe({
      next: (data) => this.renderizarTendenciaDinamica(data),
      error: () => {}
    });
  }

  renderizarGraficosPlotly(): void {
    setTimeout(() => {
      if (this.graficos?.por_departamento && this.graficoDepartamentos) {
        Plotly.react(this.graficoDepartamentos.nativeElement,
          this.graficos.por_departamento.data,
          this.graficos.por_departamento.layout);
      }
      if (this.graficos?.por_tipo_delito && this.graficoDelitos) {
        Plotly.react(this.graficoDelitos.nativeElement,
          this.graficos.por_tipo_delito.data,
          this.graficos.por_tipo_delito.layout);
      }
    }, 500);
    this.cargarTendenciaDinamica();
  }

  renderizarTendenciaDinamica(data: any): void {
    setTimeout(() => {
      if (data?.data && data?.layout && this.graficoTendencia) {
        Plotly.react(this.graficoTendencia.nativeElement, data.data, data.layout);
      }
    }, 300);
  }

  ejecutarPrediccion(): void {
    this.cargando = true;
    this.prediccion = null;

    const anio = this.filtro.anio;
    const dpto = this.filtro.dpto_hecho_new === TODO_EL_PERU ? undefined : this.filtro.dpto_hecho_new;
    const tipo = this.filtro.es_delito_x === TODOS ? undefined : this.filtro.es_delito_x;
    const mes = this.filtro.periodo === ANUAL ? undefined : parseInt(this.filtro.periodo as string);

    this.predService.predecirGeneral(anio, dpto, tipo, mes).subscribe({
      next: (res) => this.onPrediccionResult(res),
      error: () => this.cargando = false
    });
  }

  private onPrediccionResult(res: any): void {
    this.prediccion = res;
    this.cargando = false;
    this.actualizarAlerta(res.nivel_alerta);
    this.renderizarPrediccion(res);
    this.reproducirAlerta(res.nivel_alerta);
  }

  reproducirAlerta(nivel: string): void {
    if (!this.config.sonidoAlerta) return;
    try {
      const ctx = new AudioContext();
      const nivelMap: Record<string, { freq: number; duration: number; repeat: number }> = {
        'BAJO':   { freq: 880,  duration: 0.15, repeat: 1 },
        'MEDIO':  { freq: 660,  duration: 0.25, repeat: 2 },
        'ALTO':   { freq: 440,  duration: 0.3,  repeat: 3 },
        'CRITICO':{ freq: 330,  duration: 0.2,  repeat: 5 }
      };
      const cfg = nivelMap[nivel] || nivelMap['BAJO'];
      for (let i = 0; i < cfg.repeat; i++) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = nivel === 'CRITICO' ? 'sawtooth' : 'sine';
        osc.frequency.value = cfg.freq;
        gain.gain.setValueAtTime(0.3, ctx.currentTime + i * (cfg.duration + 0.1));
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + i * (cfg.duration + 0.1) + cfg.duration);
        osc.start(ctx.currentTime + i * (cfg.duration + 0.1));
        osc.stop(ctx.currentTime + i * (cfg.duration + 0.1) + cfg.duration);
      }
    } catch {}
  }

  actualizarAlerta(nivel: string): void {
    this.alertaClase = nivel || 'BAJO';
  }

  renderizarPrediccion(res: any): void {
    setTimeout(() => {
      if (!this.graficoPrediccion) return;
      const esMensual = res.tipo_periodo === 'MENSUAL';
      const valor = res.total_general || res.total_nacional || res.prediccion_total_delitos || 0;
      const label = esMensual
        ? `${res.mes_nombre} ${res.anio}`
        : `Proyección ${res.anio}`;

      const data: any = [{
        x: [label],
        y: [valor],
        type: 'bar',
        marker: { color: res.nivel_alerta === 'CRITICO' ? '#ef4444' : '#3b82f6' }
      }];
      const layout: any = {
        title: esMensual ? `Proyección Mensual - ${res.mes_nombre} ${res.anio}` : 'Proyección Anual',
        yaxis: { title: 'Delitos Proyectados' },
        height: 400
      };
      Plotly.react(this.graficoPrediccion.nativeElement, data, layout);
    }, 300);
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
