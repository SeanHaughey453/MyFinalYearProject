import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ScheduleComponent } from './schedule-page/schedule-page.component';
import { MyPlanningComponent } from './my-planning/my-planning.component';
import { MyTrackerComponent } from './my-tracker/my-tracker.component';
import { PersonalTrainersComponent } from './personal-trainers/personal-trainers.component';
import { AdminPageComponent } from './admin-page/admin-page.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'schedulepage',
    component: ScheduleComponent
  },
  {
    path: 'myplanning',
    component: MyPlanningComponent
  },
  {
    path: 'mytracker',
    component: MyTrackerComponent
  },
  {
    path: 'personaltrainers',
    component: PersonalTrainersComponent
  },
  {
    path: 'adminpage',
    component: AdminPageComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
