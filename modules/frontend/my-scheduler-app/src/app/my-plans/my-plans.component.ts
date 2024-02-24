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
  plan_list: any = [];
  planForm: any;
  planToClient: any;


  constructor(public plansService: PlansService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.plan_list = this.plansService.getPlans();

    this.planForm = this.formBuilder.group({
      name: ['', Validators.required],
      planType: ['', Validators.required],
      documentUrl: ['', Validators.required],
      tailoredTo: ['', Validators.required]
      });

    this.planToClient = this.formBuilder.group({
      clientID: ['', Validators.required],
      planID: ['', Validators.required]
    })

  }


  isInvalid(control: any) {
    return this.planForm.controls[control].invalid && 
    this.planForm.controls[control].touched;
    }
  isUntouched() {
    return this.planForm.controls.name.pristine ||
    this.planForm.controls.planType.pristine||
    this.planForm.controls.documentUrl.pristine||
    this.planForm.controls.tailoredTo.pristine;
    }
  isIncomplete() {
    return this.isInvalid('name') ||
    this.isInvalid('planType') ||
    this.isInvalid('documentUrl') ||
    this.isInvalid('tailoredTo') ||
    this.isUntouched();
    }
    
    //validation fields for assigning plans to clients
    isInvalid1(control: any) {
      return this.planToClient.controls[control].invalid && 
      this.planToClient.controls[control].touched;
      }
    isUntouched1() {
      return this.planToClient.controls.clientID.pristine ||
      this.planToClient.controls.planID.pristine;
      }
    isIncomplete1() {
      return this.isInvalid1('clientID') ||
      this.isInvalid1('planID') ||
      this.isUntouched1();
      }



    onSubmit() {
      this.plansService.postPlan(this.planForm.value)
      .subscribe({
        next: _ => {
          this.planToClient.reset();
          location.reload();  
          //this.router.navigateByUrl('/schedulepage');  
        },
        error: err => {
          console.error('Plan Form error:', err);
          this.openErrorModal('Error has prevented you from submitting the form. Please try again.');
        }
     });
    }

    onSubmitPlansToClients() {
      this.plansService.giveClientPlan(this.planToClient.value)
      .subscribe({
        next: _ => {
          this.planToClient.reset();
          location.reload();  
          //this.router.navigateByUrl('/schedulepage');  
        },
        error: err => {
          console.error('Plan Form error:', err);
          this.openErrorModal('Error has prevented you from submitting the form. Please try again.');
        }
     });
    }

  copyToClipboard(text: string) {
      navigator.clipboard.writeText(text).then(() => {
        console.log('Plan ID copied to clipboard');
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