import { Djing } from "@/djing";

declare global {
  var createDjingApp: (config: any) => Djing;
  var Djing: Djing

  interface Window {
    createDjingApp: (config: any) => Djing;
    Djing: Djing;
  }
}

window.createDjingApp = (config: any) => new Djing(config);
