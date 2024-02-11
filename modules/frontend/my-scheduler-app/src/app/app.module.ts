import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';


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
    ScheduleComponent
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
    NgbModule
    
  ],
  providers: [ScheduleService, AccountService, StaffAccountService],
  bootstrap: [AppComponent]
})
export class AppModule { }
