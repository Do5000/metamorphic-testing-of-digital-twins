import { type Module, inject } from 'langium';
import { createDefaultModule, createDefaultSharedModule, type DefaultSharedModuleContext, type LangiumServices, type LangiumSharedServices, type PartialLangiumServices } from 'langium/lsp';
import { MtDslGeneratedModule, MtDslGeneratedSharedModule } from './generated/module.js';

export type MtDslServices = LangiumServices & {
    // add custom services here
};

export const MtDslModule: Module<MtDslServices, PartialLangiumServices> = {
    // custom services can be defined here
};

export function createMtDslServices(context: DefaultSharedModuleContext): {
    shared: LangiumSharedServices,
    MtDsl: MtDslServices
} {
    const shared = inject(
        createDefaultSharedModule(context),
        MtDslGeneratedSharedModule
    );
    const MtDsl = inject(
        createDefaultModule({ shared }),
        MtDslGeneratedModule,
        MtDslModule
    );
    shared.ServiceRegistry.register(MtDsl);
    return { shared, MtDsl };
}
