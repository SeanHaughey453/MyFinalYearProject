import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { PlansService } from "../services/plan.service";

@Component({
  selector: 'myalterschedule',
  templateUrl: './my-alter-schedule.component.html',
  styleUrls: ['./my-alter-schedule.component.css']
})
export class MyAlterScheduleComponent {


  constructor(public plansService: PlansService,  
              public dialog: MatDialog
              ) { }

  ngOnInit() {


  }
  onClick() {
    this.plansService.getPlans()
    .subscribe({
      next: _ => {},
      error: err => {
        console.error('Alter schedule errror:', err);
        this.openErrorModal('somthing went wrong wrong wrong. Please try again.');
      }
});
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}