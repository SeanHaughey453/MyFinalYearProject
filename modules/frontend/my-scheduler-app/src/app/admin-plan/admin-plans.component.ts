import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { PlansService } from "../services/plan.service";

@Component({
  selector: 'adminplans',
  templateUrl: './admin-plans.component.html',
  styleUrls: ['./admin-plans.component.css']
})
export class AdminPlansComponent {
  plan_list: any = [];
  planForm: any;
  planToClient: any;


  constructor(public plansService: PlansService,  
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.plan_list = this.plansService.getPlans();



  }
    removePlan(planId: string) {
      this.plansService.deletePlan(planId).subscribe({
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