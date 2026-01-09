/**
 * CNPJ (Cadastro Nacional de Pessoa Jurídica) Value Object
 *
 * Brazilian company taxpayer registry identification with validation.
 * Validates format (14 digits), rejects known invalid sequences, and verifies check digits.
 *
 * @see CENTRAL/BUSINESS-RULES/VALIDATION-RULES/cnpj-validation.md
 */

import { ValidationError } from './cpf.js'

export class CNPJ {
  private readonly value: string

  /**
   * Creates a new CNPJ instance
   * @param cnpj - CNPJ string (formatted "##.###.###/####-##" or raw "##############")
   * @throws {ValidationError} If CNPJ is invalid
   */
  constructor(cnpj: string) {
    if (!CNPJ.validate(cnpj)) {
      throw new ValidationError('CNPJ inválido')
    }
    this.value = CNPJ.normalize(cnpj)
  }

  /**
   * Validates a CNPJ string
   * @param cnpj - CNPJ to validate
   * @returns true if valid, false otherwise
   */
  static validate(cnpj: string): boolean {
    if (!cnpj) return false

    // Normalize: remove non-numeric characters
    const normalized = CNPJ.normalize(cnpj)

    // Must have exactly 14 digits
    if (normalized.length !== 14) return false

    // Reject known invalid sequences (all same digit)
    if (/^(\d)\1{13}$/.test(normalized)) return false

    // Validate first check digit
    const firstDigit = CNPJ.calculateCheckDigit(normalized.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    const twelfthDigit = normalized[12]
    if (!twelfthDigit || firstDigit !== parseInt(twelfthDigit, 10)) return false

    // Validate second check digit
    const secondDigit = CNPJ.calculateCheckDigit(normalized.slice(0, 13), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    const thirteenthDigit = normalized[13]
    if (!thirteenthDigit || secondDigit !== parseInt(thirteenthDigit, 10)) return false

    return true
  }

  /**
   * Normalizes CNPJ by removing all non-numeric characters
   * @param cnpj - CNPJ string
   * @returns Normalized CNPJ (14 digits only)
   */
  static normalize(cnpj: string): string {
    return cnpj.replace(/\D/g, '')
  }

  /**
   * Calculates check digit using mod 11 algorithm with custom weights
   * @param digits - Digit string
   * @param weights - Weight array
   * @returns Check digit (0-9)
   */
  private static calculateCheckDigit(digits: string, weights: number[]): number {
    let sum = 0
    for (let i = 0; i < digits.length; i++) {
      const digit = digits[i]
      const weight = weights[i]
      if (digit !== undefined && weight !== undefined) {
        sum += parseInt(digit, 10) * weight
      }
    }
    const remainder = sum % 11
    return remainder < 2 ? 0 : 11 - remainder
  }

  /**
   * Formats CNPJ as ##.###.###/####-##
   * @returns Formatted CNPJ string
   */
  format(): string {
    return this.value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
  }

  /**
   * Returns raw CNPJ value (14 digits)
   * @returns Normalized CNPJ string
   */
  toString(): string {
    return this.value
  }

  /**
   * Returns raw CNPJ value for JSON serialization
   * @returns Normalized CNPJ string
   */
  toJSON(): string {
    return this.value
  }

  /**
   * Checks equality with another CNPJ
   * @param other - Another CNPJ instance
   * @returns true if equal
   */
  equals(other: CNPJ): boolean {
    return this.value === other.value
  }
}
