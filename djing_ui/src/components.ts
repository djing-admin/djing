import camelCase from 'lodash/camelCase';
import upperFirst from 'lodash/upperFirst';

import CustomError404 from '@/views/CustomError404.vue';
import CustomError403 from '@/views/CustomError403.vue';
import CustomAppError from '@/views/CustomAppError.vue';
import ResourceIndex from '@/views/Index.vue';
import ResourceLens from '@/views/Lens.vue';
import ResourceDetail from '@/views/Detail.vue';
import Attach from '@/views/Attach.vue';
import UpdateAttached from '@/views/UpdateAttached.vue';

async function registerComponents(app: any, importComponents: Record<string, any>, type: string = '') {
  const files = Object.keys(importComponents);
  for (const fileName of files) {
    try {
      const componentConfig = importComponents[fileName]; // Direct access since eager is true
      const componentName = upperFirst(
        camelCase(
          fileName
            .split('/')
            .pop()!
            .replace(/\.\w+$/, '')
        )
      );

      app.component(`${type}${componentName}`, componentConfig.default || componentConfig);
    } catch (error) {
      console.error(`Error loading component ${fileName}:`, error);
    }
  }
}

export async function registerViews(app: any) {
  app.component('CustomError403', CustomError403);
  app.component('CustomError404', CustomError404);
  app.component('CustomAppError', CustomAppError);
  app.component('ResourceIndex', ResourceIndex);
  app.component('ResourceLens', ResourceLens);
  app.component('ResourceDetail', ResourceDetail);
  app.component('AttachResource', Attach);
  app.component('UpdateAttachedResource', UpdateAttached);

  const componentImports = import.meta.glob('./components/**/*.vue', { eager: true }); // Eager import

  registerComponents(app, componentImports);
}

export async function registerFields(app: any) {
  const indexComponents = import.meta.glob('./fields/Index/*.vue', { eager: true }); // Eager import
  const detailComponents = import.meta.glob('./fields/Detail/*.vue', { eager: true }); // Eager import
  const formComponents = import.meta.glob('./fields/Form/*.vue', { eager: true }); // Eager import
  const filterComponents = import.meta.glob('./fields/Filter/*.vue', { eager: true }); // Eager import

  registerComponents(app, indexComponents, 'Index');
  registerComponents(app, detailComponents, 'Detail');
  registerComponents(app, formComponents, 'Form');
  registerComponents(app, filterComponents, 'Filter');
}
