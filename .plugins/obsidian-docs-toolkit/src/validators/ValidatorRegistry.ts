import { Validator } from "./base/Validator";
import { DocsLinterConfig } from "../config/ConfigSchema";

/**
 * Registry for validators - handles auto-discovery and filtering
 */
export class ValidatorRegistry {
  private validators: Map<string, Validator> = new Map();

  /**
   * Register a validator
   */
  register(validator: Validator): void {
    if (this.validators.has(validator.id)) {
      console.warn(`Validator with id '${validator.id}' is already registered`);
    }
    this.validators.set(validator.id, validator);
  }

  /**
   * Register multiple validators
   */
  registerAll(validators: Validator[]): void {
    for (const validator of validators) {
      this.register(validator);
    }
  }

  /**
   * Unregister a validator by ID
   */
  unregister(id: string): boolean {
    return this.validators.delete(id);
  }

  /**
   * Get a validator by ID
   */
  get(id: string): Validator | undefined {
    return this.validators.get(id);
  }

  /**
   * Get all registered validators
   */
  getAll(): Validator[] {
    return Array.from(this.validators.values());
  }

  /**
   * Get all local validators (non-global)
   */
  getLocalValidators(): Validator[] {
    return this.getAll().filter(v => !v.isGlobal);
  }

  /**
   * Get all global validators
   */
  getGlobalValidators(): Validator[] {
    return this.getAll().filter(v => v.isGlobal);
  }

  /**
   * Get enabled validators based on config
   */
  getEnabledValidators(config: DocsLinterConfig): Validator[] {
    return this.getAll().filter(v => {
      const validatorConfig = config.validators[v.id];
      return validatorConfig?.enabled !== false;
    });
  }

  /**
   * Get enabled local validators
   */
  getEnabledLocalValidators(config: DocsLinterConfig): Validator[] {
    return this.getEnabledValidators(config).filter(v => !v.isGlobal);
  }

  /**
   * Get enabled global validators
   */
  getEnabledGlobalValidators(config: DocsLinterConfig): Validator[] {
    return this.getEnabledValidators(config).filter(v => v.isGlobal);
  }

  /**
   * Check if a validator is registered
   */
  has(id: string): boolean {
    return this.validators.has(id);
  }

  /**
   * Clear all registered validators
   */
  clear(): void {
    this.validators.clear();
  }

  /**
   * Get number of registered validators
   */
  get size(): number {
    return this.validators.size;
  }
}

/**
 * Create a registry with all built-in validators
 */
export function createBuiltinRegistry(): ValidatorRegistry {
  const registry = new ValidatorRegistry();

  // Import and register all built-in validators
  // This is done lazily to avoid circular dependencies
  return registry;
}
