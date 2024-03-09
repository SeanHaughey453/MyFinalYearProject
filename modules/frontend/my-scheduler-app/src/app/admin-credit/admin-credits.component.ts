import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";
import { CreditsService } from "../services/credit.service";

@Component({
  selector: 'admincredits',
  templateUrl: './admin-credits.component.html',
  styleUrls: ['./admin-credits.component.css']
})
export class AdminCreditsComponent {
  credit_list: any = [];
  creditForm: any;
  creditToClient: any;


  constructor(public creditsService: CreditsService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.credit_list = this.creditsService.getAllCredits();
  
  }
  
  removeCredit(creditId: string) {
      this.creditsService.deleteCredit(creditId).subscribe({
        next: () => {location.reload(); },
        error: (error) => {console.error('Error removing client:', error);}
      });
    }



  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}