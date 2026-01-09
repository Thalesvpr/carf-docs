/**
 * Phone (Brazilian Phone Number) Value Object
 *
 * Brazilian phone number with DDD validation.
 * Supports landline (8 digits) and mobile (9 digits starting with 9).
 * Format: (##) ####-#### or (##) #####-####
 *
 * @see CENTRAL/BUSINESS-RULES/VALIDATION-RULES/phone-validation.md
 */

import { ValidationError } from './cpf.js'

export class Phone {
  private readonly value: string
  private readonly ddd: string
  private readonly number: string

  /**
   * Creates a new Phone instance
   * @param phone - Phone string (formatted "(##) ####-####" / "(##) #####-####" or raw "##########" / "###########")
   * @throws {ValidationError} If phone is invalid
   */
  constructor(phone: string) {
    if (!Phone.validate(phone)) {
      throw new ValidationError('Telefone inválido')
    }

    const normalized = Phone.normalize(phone)
    this.value = normalized
    this.ddd = normalized.slice(0, 2)
    this.number = normalized.slice(2)
  }

  /**
   * Validates a Brazilian phone number
   * @param phone - Phone to validate
   * @returns true if valid, false otherwise
   */
  static validate(phone: string): boolean {
    if (!phone) return false

    // Normalize: remove non-numeric characters
    const normalized = Phone.normalize(phone)

    // Must have 10 (landline) or 11 (mobile) digits
    if (normalized.length !== 10 && normalized.length !== 11) return false

    // Extract DDD (first 2 digits)
    const ddd = parseInt(normalized.slice(0, 2), 10)

    // Valid DDD ranges: 11-99 (excluding some invalid ranges)
    if (ddd < 11 || ddd > 99) return false

    // Mobile numbers (11 digits) must start with 9
    if (normalized.length === 11) {
      const firstDigit = normalized[2]
      if (firstDigit !== '9') return false
    }

    return true
  }

  /**
   * Normalizes phone by removing all non-numeric characters
   * @param phone - Phone string
   * @returns Normalized phone (10 or 11 digits)
   */
  static normalize(phone: string): string {
    return phone.replace(/\D/g, '')
  }

  /**
   * Formats phone as (##) ####-#### or (##) #####-####
   * @returns Formatted phone string
   */
  format(): string {
    if (this.value.length === 11) {
      // Mobile: (##) #####-####
      return this.value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
    } else {
      // Landline: (##) ####-####
      return this.value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3')
    }
  }

  /**
   * Returns raw phone value (10 or 11 digits)
   * @returns Normalized phone string
   */
  toString(): string {
    return this.value
  }

  /**
   * Returns raw phone value for JSON serialization
   * @returns Normalized phone string
   */
  toJSON(): string {
    return this.value
  }

  /**
   * Checks equality with another Phone
   * @param other - Another Phone instance
   * @returns true if equal
   */
  equals(other: Phone): boolean {
    return this.value === other.value
  }

  /**
   * Returns DDD (area code)
   * @returns DDD string (2 digits)
   */
  getDDD(): string {
    return this.ddd
  }

  /**
   * Returns phone number without DDD
   * @returns Number string (8 or 9 digits)
   */
  getNumber(): string {
    return this.number
  }

  /**
   * Checks if phone is mobile (11 digits)
   * @returns true if mobile
   */
  isMobile(): boolean {
    return this.value.length === 11
  }

  /**
   * Checks if phone is landline (10 digits)
   * @returns true if landline
   */
  isLandline(): boolean {
    return this.value.length === 10
  }
}
