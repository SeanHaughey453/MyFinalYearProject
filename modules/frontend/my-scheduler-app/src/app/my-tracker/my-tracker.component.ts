import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { StaffAccountService } from '../services/staffAccount.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { AccountService } from '../services/account.service';
import { Observable } from 'rxjs';



@Component({
 selector: 'mytracker',
 templateUrl: './my-tracker.component.html',
 styleUrls: ['./my-tracker.component.css']
})

export class MyTrackerComponent {
    model: any = {}
    loginError: boolean = false;
    plan_list: any = []
    numCredits: any;
    constructor(
                public router: Router, 
                public accountService: AccountService,
                public dialog: MatDialog
                ) {}

    ngOnInit(): void {
        if (this.accountService.currentUser$) 
        {
            this.accountService.currentUser$.subscribe(user => {});
            
        }
        this.plan_list = this.accountService.getClientsPlans();

        this.accountService.getClientsNumCredits().subscribe((data: any) => {
          this.numCredits = data.numCredits;
      });
    }

      openErrorModal(errorMessage: string): void {
        this.dialog.open(ErrorModalComponent, {
          data: errorMessage,
        });
      }

 }