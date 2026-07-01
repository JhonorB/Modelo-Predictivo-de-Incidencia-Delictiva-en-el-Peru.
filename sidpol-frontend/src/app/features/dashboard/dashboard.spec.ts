// @ts-nocheck
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardComponent } from './dashboard'; // <-- Nombre exacto de la clase exportada

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('debería crear el componente del dashboard', () => {
    expect(component).toBeTruthy();
  });
});
