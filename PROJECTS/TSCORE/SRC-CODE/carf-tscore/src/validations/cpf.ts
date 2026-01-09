/**
 * CPF (Cadastro de Pessoa Física) Value Object
 *
 * Brazilian individual taxpayer registry identification with validation.
 * Validates format (11 digits), rejects known invalid sequences, and verifies check digits.
 *
 * @see CENTRAL/BUSINESS-RULES/VALIDATION-RULES/cpf-validation.md
 */

export class ValidationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ValidationError'
  }
}

export class CPF {
  private readonly value: string

  /**
   * Creates a new CPF instance
   * @param cpf - CPF string (formatted "###.###.###-##" or raw "###########")
   * @throws {ValidationError} If CPF is invalid
   */
  constructor(cpf: string) {
    if (!CPF.validate(cpf)) {
      throw new ValidationError('CPF inválido')
    }
    this.value = CPF.normalize(cpf)
  }

  /**
   * Validates a CPF string
   * @param cpf - CPF to validate
   * @returns true if valid, false otherwise
   */
  static validate(cpf: string): boolean {
    if (!cpf) return false

    // Normalize: remove non-numeric characters
    const normalized = CPF.normalize(cpf)

    // Must have exactly 11 digits
    if (normalized.length !== 11) return false

    // Reject known invalid sequences (all same digit)
    if (/^(\d)\1{10}$/.test(normalized)) return false

    // Validate first check digit
    const firstDigit = CPF.calculateCheckDigit(normalized.slice(0, 9), 10)
    const ninthDigit = normalized[9]
    if (!ninthDigit || firstDigit !== parseInt(ninthDigit, 10)) return false

    // Validate second check digit
    const secondDigit = CPF.calculateCheckDigit(normalized.slice(0, 10), 11)
    const tenthDigit = normalized[10]
    if (!tenthDigit || secondDigit !== parseInt(tenthDigit, 10)) return false

    return true
  }

  /**
   * Normalizes CPF by removing all non-numeric characters
   * @param cpf - CPF string
   * @returns Normalized CPF (11 digits only)
   */
  static normalize(cpf: string): string {
    return cpf.replace(/\D/g, '')
  }

  /**
   * Calculates check digit using mod 11 algorithm
   * @param digits - Digit string
   * @param weight - Initial weight (10 for first digit, 11 for second)
   * @returns Check digit (0-9)
   */
  private static calculateCheckDigit(digits: string, weight: number): number {
    let sum = 0
    for (let i = 0; i < digits.length; i++) {
      const digit = digits[i]
      if (digit !== undefined) {
        sum += parseInt(digit, 10) * (weight - i)
      }
    }
    const remainder = sum % 11
    return remainder < 2 ? 0 : 11 - remainder
  }

  /**
   * Formats CPF as ###.###.###-##
   * @returns Formatted CPF string
   */
  format(): string {
    return this.value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
  }

  /**
   * Returns raw CPF value (11 digits)
   * @returns Normalized CPF string
   */
  toString(): string {
    return this.value
  }

  /**
   * Returns raw CPF value for JSON serialization
   * @returns Normalized CPF string
   */
  toJSON(): string {
    return this.value
  }

  /**
   * Checks equality with another CPF
   * @param other - Another CPF instance
   * @returns true if equal
   */
  equals(other: CPF): boolean {
    return this.value === other.value
  }
}
