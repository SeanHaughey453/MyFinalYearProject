import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ScheduleComponent } from './schedule-page/schedule-page.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
    },
    {
      path: 'schedulepage',
      component: ScheduleComponent
      }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
