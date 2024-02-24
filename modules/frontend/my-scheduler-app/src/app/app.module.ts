import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { NavComponent } from './nav/nav.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent} from './login/login.component';
import { ErrorModalComponent } from './error-modal/error-modal.component';
import { StaffRegisterComponent } from './staff-register/staff-register.component';
import { StaffLoginComponent } from './staff-login/staff-login.component';
import { ScheduleComponent } from './schedule-page/schedule-page.component';
import { ScheduleService } from './services/schedule.service';
import { AccountService } from './services/account.service';
import { StaffAccountService } from './services/staffAccount.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MyPlanningComponent } from './my-planning/my-planning.component';
import { PlansService } from './services/plan.service';
import { MyPlansComponent } from './my-plans/my-plans.component';
import { CreditsService } from './services/credit.service';
import { MyCreditsComponent } from './my-credits/my-credits.component';
import { MyAlterScheduleComponent } from './my-alter-schedule/my-alter-schedule.component';


// var routes: any = [
//   {
//     path: '',
//     component: HomeComponent
//     }

// ];

@NgModule({
  declarations: [
    AppComponent, 
    HomeComponent,
    NavComponent,
    ErrorModalComponent,
    RegisterComponent,
    LoginComponent,
    StaffRegisterComponent,
    StaffLoginComponent,
    ScheduleComponent,
    MyPlanningComponent,
    MyPlansComponent,
    MyCreditsComponent,
    MyAlterScheduleComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatDialogModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatSelectModule,
    NgbModule,
    BsDropdownModule.forRoot() 
    
  ],
  providers: [ScheduleService, AccountService, StaffAccountService, PlansService, CreditsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
