import { type Module, inject } from 'langium';
import { createDefaultModule, createDefaultSharedModule, type DefaultSharedModuleContext, type LangiumServices, type LangiumSharedServices, type PartialLangiumServices } from 'langium/lsp';
import { MtDslGeneratedModule, MtDslGeneratedSharedModule } from './generated/module.js';
import { MtDslValidator, registerValidationChecks } from './mt-dsl-validator.js';

export type MtDslAddedServices = {
    validation: {
        MtDslValidator: MtDslValidator
    }
}

export type MtDslServices = LangiumServices & MtDslAddedServices;

export const MtDslModule: Module<MtDslServices, PartialLangiumServices & MtDslAddedServices> = {
    validation: {
        MtDslValidator: () => new MtDslValidator()
    }
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
    registerValidationChecks(MtDsl);
    return { shared, MtDsl };
}
