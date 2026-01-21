export { FrontmatterValidator } from "./FrontmatterValidator";
export { SectionsValidator } from "./SectionsValidator";
export { NamingValidator } from "./NamingValidator";
export { TitleValidator } from "./TitleValidator";
export { WordCountValidator } from "./WordCountValidator";
export { ForbiddenPatternsValidator } from "./ForbiddenPatternsValidator";
export { LinksValidator } from "./LinksValidator";
export { StaleValidator } from "./StaleValidator";
export { OrphansValidator } from "./OrphansValidator";
export { EmptyFoldersValidator } from "./EmptyFoldersValidator";

import { ValidatorRegistry } from "../ValidatorRegistry";
import { FrontmatterValidator } from "./FrontmatterValidator";
import { SectionsValidator } from "./SectionsValidator";
import { NamingValidator } from "./NamingValidator";
import { TitleValidator } from "./TitleValidator";
import { WordCountValidator } from "./WordCountValidator";
import { ForbiddenPatternsValidator } from "./ForbiddenPatternsValidator";
import { LinksValidator } from "./LinksValidator";
import { StaleValidator } from "./StaleValidator";
import { OrphansValidator } from "./OrphansValidator";
import { EmptyFoldersValidator } from "./EmptyFoldersValidator";

/**
 * Create a registry with all built-in validators registered
 */
export function createBuiltinValidatorRegistry(): ValidatorRegistry {
  const registry = new ValidatorRegistry();

  registry.registerAll([
    new FrontmatterValidator(),
    new SectionsValidator(),
    new NamingValidator(),
    new TitleValidator(),
    new WordCountValidator(),
    new ForbiddenPatternsValidator(),
    new LinksValidator(),
    new StaleValidator(),
    new OrphansValidator(),
    new EmptyFoldersValidator()
  ]);

  return registry;
}
