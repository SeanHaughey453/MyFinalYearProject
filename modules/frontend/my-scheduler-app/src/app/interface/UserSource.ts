import { BehaviorSubject } from "rxjs";
import { User } from "../user/user";

export interface UserSource {
     currentUserSource: BehaviorSubject<User | null>;
  }