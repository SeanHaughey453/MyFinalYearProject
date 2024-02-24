import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { StaffAccountService } from '../services/staffAccount.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { AccountService } from '../services/account.service';



@Component({
 selector: 'myplanning',
 templateUrl: './my-planning.component.html',
 styleUrls: ['./my-planning.component.css']
})

export class MyPlanningComponent {
    model: any = {}
    loginError: boolean = false;
    planSwitch: boolean = false;
    creditSwitch: boolean = false;
    scheduleSwitch: boolean = false;
    client_list: any = []
    constructor(
                public router: Router, 
                public staffAccountService: StaffAccountService,
                public accountService: AccountService,
                public dialog: MatDialog
                ) {}

    ngOnInit(): void {
        if (this.staffAccountService.currentUser$) 
        {
            this.staffAccountService.currentUser$.subscribe(user => {});
            
        }
        this.client_list = this.accountService.getClients();
    }

      openErrorModal(errorMessage: string): void {
        this.dialog.open(ErrorModalComponent, {
          data: errorMessage,
        });
      }

      planBool(){
        this.planSwitch = !this.planSwitch
      }

      cancelPlanMode(event: boolean) {
        this.planSwitch = event;
      }

      creditBool(){
        this.creditSwitch = !this.creditSwitch
      }

      cancelCreditMode(event: boolean) {
        this.creditSwitch = event;
      }

      scheduleBool(){
        this.scheduleSwitch = !this.scheduleSwitch
      }

      cancelScheduleMode(event: boolean) {
        this.scheduleSwitch = event;
      }


      copyToClipboard(text: string) {
        navigator.clipboard.writeText(text).then(() => {
          console.log('ID copied to clipboard');
        }).catch(err => {
          console.error('Could not copy text: ', err);
        });
      }

    
 }