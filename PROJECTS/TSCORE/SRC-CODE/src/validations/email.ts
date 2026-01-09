/**
 * Email Value Object
 *
 * Email address with RFC 5322 validation (simplified regex).
 *
 * @see CENTRAL/BUSINESS-RULES/VALIDATION-RULES/email-validation.md
 */

import { ValidationError } from './cpf.js'

export class Email {
  private readonly value: string

  /**
   * Creates a new Email instance
   * @param email - Email string
   * @throws {ValidationError} If email is invalid
   */
  constructor(email: string) {
    if (!Email.validate(email)) {
      throw new ValidationError('Email inválido')
    }
    this.value = email.toLowerCase().trim()
  }

  /**
   * Validates an email address using simplified RFC 5322 regex
   * @param email - Email to validate
   * @returns true if valid, false otherwise
   */
  static validate(email: string): boolean {
    if (!email) return false

    // Simplified RFC 5322 regex (basic validation)
    // Full RFC 5322 is extremely complex, this covers 99% of cases
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

    const normalized = email.trim()

    // Basic checks
    if (normalized.length === 0) return false
    if (normalized.length > 254) return false // RFC 5321 max length
    if (!emailRegex.test(normalized)) return false

    // Check parts
    const [localPart, domain] = normalized.split('@')
    if (!localPart || !domain) return false
    if (localPart.length > 64) return false // RFC 5321 local part max
    if (domain.length > 255) return false // RFC 5321 domain max

    // Require at least one dot in domain (TLD required)
    if (!domain.includes('.')) return false

    return true
  }

  /**
   * Returns email value (lowercased and trimmed)
   * @returns Email string
   */
  toString(): string {
    return this.value
  }

  /**
   * Returns email value for JSON serialization
   * @returns Email string
   */
  toJSON(): string {
    return this.value
  }

  /**
   * Checks equality with another Email
   * @param other - Another Email instance
   * @returns true if equal
   */
  equals(other: Email): boolean {
    return this.value === other.value
  }

  /**
   * Gets domain part of email
   * @returns Domain string (e.g., "example.com")
   */
  getDomain(): string {
    return this.value.split('@')[1]
  }

  /**
   * Gets local part of email
   * @returns Local part string (e.g., "user")
   */
  getLocalPart(): string {
    return this.value.split('@')[0]
  }
}
