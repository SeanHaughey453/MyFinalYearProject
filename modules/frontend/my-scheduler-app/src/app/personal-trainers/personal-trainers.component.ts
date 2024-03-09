import { Component } from '@angular/core';
import { AccountService } from '../services/account.service';




@Component({
 selector: 'personaltrainers',
 templateUrl: './personal-trainers.component.html',
 styleUrls: ['./personal-trainers.component.css']
})

export class PersonalTrainersComponent {
    trainer_list: any = [];
    constructor(
        public accountService: AccountService,
                ) {}

    ngOnInit(): void { 
        this.trainer_list = this.accountService.getStaffProtected();
      }


    
 }