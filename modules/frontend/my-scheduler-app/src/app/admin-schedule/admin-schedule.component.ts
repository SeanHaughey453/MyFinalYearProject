import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { PlansService } from "../services/plan.service";
import { ScheduleService } from "../services/schedule.service";

@Component({
  selector: 'adminschedule',
  templateUrl: './admin-schedule.component.html',
  styleUrls: ['./admin-schedule.component.css']
})
export class AdminScheduleComponent {
  schedule_list: any = [];



  constructor(public scheduleService: ScheduleService,  
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.schedule_list = this.scheduleService.getAllSchedules();
  }
  
  removeSchedule(scheduleId: string) {
      this.scheduleService.deleteSchedule(scheduleId).subscribe({
        next: () => {
          location.reload(); 
        },
        error: (error) => {
          console.error('Error removing client:', error);
        }
      });
    }


  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}