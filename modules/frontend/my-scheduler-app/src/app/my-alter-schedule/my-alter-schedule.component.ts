import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";
import { ScheduleService } from "../services/schedule.service";

@Component({
  selector: 'myalterschedule',
  templateUrl: './my-alter-schedule.component.html',
  styleUrls: ['./my-alter-schedule.component.css']
})
export class MyAlterScheduleComponent {

  nonClientList: any = [];
  addClientForm: any;


  constructor(public dialog: MatDialog,
              public staffAccountService: StaffAccountService,
              private formBuilder: FormBuilder,
              public scheduleService: ScheduleService
              ) { }

  ngOnInit() {
    this.nonClientList = this.staffAccountService.getNonClients();

    this.addClientForm = this.formBuilder.group({
      client: ['', Validators.required],
      });
  }

  isInvalid(control: any) {
    return this.addClientForm.controls[control].invalid && 
    this.addClientForm.controls[control].touched;
    }
  isUntouched() {
    return this.addClientForm.controls.client.pristine;
    }
  isIncomplete() {
    return this.isInvalid('client')||
    this.isUntouched();
    }

  onSubmit() {
      this.staffAccountService.addClient(this.addClientForm.value)
      .subscribe({
        next: _ => {
          this.addClientForm.reset();
          location.reload();  
          //this.router.navigateByUrl('/schedulepage');  
        },
        error: err => {
          console.error('Credit Form error:', err);
          this.openErrorModal('Error has prevented you from submitting the form. Please try again.');
        }
     });
    }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

  createNewSchedule() {
    this.scheduleService.postSchedule().subscribe({
      next: () => {location.reload(); },
      error: (error) => {console.error('Error removing client:', error);}
    });
  }

  copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('User ID copied to clipboard');
    }).catch(err => {
      console.error('Could not copy text: ', err);
    });
  }

}