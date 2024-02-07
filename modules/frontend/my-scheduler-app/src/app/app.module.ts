import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { NavComponent } from './nav/nav.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent} from './login/login.component';

import { ErrorModalComponent } from './error-modal/error-modal.component';
import { StaffRegisterComponent } from './staff-register/staff-register.component';
import { StaffLoginComponent } from './staff-login/staff-login.component';


var routes: any = [
  {
    path: '',
    component: HomeComponent
    }

];

@NgModule({
  declarations: [
    AppComponent, 
    HomeComponent,
    NavComponent,
    ErrorModalComponent,
    RegisterComponent,
    LoginComponent,
    StaffRegisterComponent,
    StaffLoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatDialogModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
