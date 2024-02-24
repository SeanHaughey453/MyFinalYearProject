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
  credit_list: any = [];
  creditForm: any;
  creditToClient: any;


  constructor(public creditsService: CreditsService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.credit_list = this.creditsService.getCredits();

    this.creditForm = this.formBuilder.group({
      planType: ['', Validators.required],
      });

    this.creditToClient = this.formBuilder.group({
      clientID: ['', Validators.required],
      creditID: ['', Validators.required]
    })
  
  }

  isInvalid(control: any) {
    return this.creditForm.controls[control].invalid && 
    this.creditForm.controls[control].touched;
    }
  isUntouched() {
    return this.creditForm.controls.planType.pristine;
    }
  isIncomplete() {
    return this.isInvalid('planType')||
    this.isUntouched();
    }
  
  onSubmit() {
      this.creditsService.postCredit(this.creditForm.value)
      .subscribe({
        next: _ => {
          this.creditForm.reset();
          location.reload();  
          //this.router.navigateByUrl('/schedulepage');  
        },
        error: err => {
          console.error('Credit Form error:', err);
          this.openErrorModal('Error has prevented you from submitting the form. Please try again.');
        }
     });
    }

  //validation fields for assigning plans to clients
  isInvalid1(control: any) {
    return this.creditToClient.controls[control].invalid && 
    this.creditToClient.controls[control].touched;
    }
  isUntouched1() {
    return this.creditToClient.controls.clientID.pristine ||
    this.creditToClient.controls.creditID.pristine;
    }
  isIncomplete1() {
    return this.isInvalid1('clientID') ||
    this.isInvalid1('creditID') ||
    this.isUntouched1();
    }
  
  
  onSubmitCreditToClients() {
      this.creditsService.giveClientCredit(this.creditToClient.value)
      .subscribe({
        next: _ => {
          this.creditToClient.reset();
          location.reload();  
          //this.router.navigateByUrl('/schedulepage');  
        },
        error: err => {
          console.error('Plan Form error:', err);
          this.openErrorModal('Error has prevented you from submitting the form. Please try again.');
        }
     });
    }

//   onClick() {
//     this.creditsService.getCredits()
//     .subscribe({
//       next: _ => {},
//       error: err => {
//         console.error('Credit error:', err);
//         this.openErrorModal('Somthing happened when retreiving all credits. Please try again.');
//       }
// });
//   }

  copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Credit ID copied to clipboard');
    }).catch(err => {
      console.error('Could not copy text: ', err);
    });
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}