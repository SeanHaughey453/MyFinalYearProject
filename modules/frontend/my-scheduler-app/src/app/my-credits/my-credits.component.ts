import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";
import { CreditsService } from "../services/credit.service";

@Component({
  selector: 'mycredits',
  templateUrl: './my-credits.component.html',
  styleUrls: ['./my-credits.component.css']
})
export class MyCreditsComponent {
  loginForm:any;


  constructor(public creditsService: CreditsService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
  
  }



  onClick() {
    this.creditsService.getCredits()
    .subscribe({
      next: _ => {},
      error: err => {
        console.error('Credit error:', err);
        this.openErrorModal('Somthing happened when retreiving all credits. Please try again.');
      }
});
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}