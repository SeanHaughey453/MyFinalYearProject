import { Component,OnInit  } from "@angular/core";
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { AdminAccountService } from "../services/adminAccount.service";

@Component({
  selector: 'adminstaff',
  templateUrl: './admin-staff.component.html',
  styleUrls: ['./admin-staff.component.css']
})
export class AdminStaffComponent {
  staff_list: any = [];



  constructor(public adminAccountService: AdminAccountService,  
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.staff_list = this.adminAccountService.getStaff();



  }
    removeStaff(planId: string) {
      this.adminAccountService.deleteStaff(planId).subscribe({
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