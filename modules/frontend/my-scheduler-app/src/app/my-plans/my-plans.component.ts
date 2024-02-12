import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";
import { PlansService } from "../services/plan.service";

@Component({
  selector: 'myplans',
  templateUrl: './my-plans.component.html',
  styleUrls: ['./my-plans.component.css']
})
export class MyPlansComponent {
  loginForm:any;


  constructor(public plansService: PlansService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    

  }



  onClick() {
    this.plansService.getPlans()
    .subscribe({
      next: _ => {},
      error: err => {
        // Handle login error
        console.error('Error Retriving Plans:', err);
        // Set a flag or property to indicate a login error (for displaying the error message)
        this.openErrorModal('There was an error retireving plans. Please try again.');
      }
});
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}