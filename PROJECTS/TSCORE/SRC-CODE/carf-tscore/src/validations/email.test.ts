import { describe, expect, test } from 'bun:test'
import { Email } from './email'
import { ValidationError } from './cpf'

describe('Email', () => {
  describe('validation', () => {
    test('should accept valid emails', () => {
      expect(() => new Email('user@example.com')).not.toThrow()
      expect(() => new Email('user.name@example.com')).not.toThrow()
      expect(() => new Email('user+tag@example.co.uk')).not.toThrow()
      expect(() => new Email('user_name@example-domain.com')).not.toThrow()
    })

    test('should reject invalid emails', () => {
      expect(() => new Email('invalid')).toThrow(ValidationError)
      expect(() => new Email('@example.com')).toThrow(ValidationError)
      expect(() => new Email('user@')).toThrow(ValidationError)
      expect(() => new Email('user @example.com')).toThrow(ValidationError)
      expect(() => new Email('user@example')).toThrow(ValidationError)
    })

    test('should reject empty email', () => {
      expect(() => new Email('')).toThrow(ValidationError)
      expect(() => new Email('   ')).toThrow(ValidationError)
    })

    test('should reject emails exceeding max lengths', () => {
      // Local part > 64 chars
      const longLocal = 'a'.repeat(65) + '@example.com'
      expect(() => new Email(longLocal)).toThrow(ValidationError)

      // Domain > 255 chars
      const longDomain = 'user@' + 'a'.repeat(256) + '.com'
      expect(() => new Email(longDomain)).toThrow(ValidationError)

      // Total > 254 chars
      const longEmail = 'a'.repeat(250) + '@abc.com'
      expect(() => new Email(longEmail)).toThrow(ValidationError)
    })
  })

  describe('normalization', () => {
    test('should lowercase and trim email', () => {
      const email = new Email('  USER@EXAMPLE.COM  ')
      expect(email.toString()).toBe('user@example.com')
    })

    test('should serialize correctly to JSON', () => {
      const email = new Email('user@example.com')
      expect(JSON.stringify({ email })).toBe('{"email":"user@example.com"}')
    })
  })

  describe('parts extraction', () => {
    test('should extract domain correctly', () => {
      const email = new Email('user@example.com')
      expect(email.getDomain()).toBe('example.com')
    })

    test('should extract local part correctly', () => {
      const email = new Email('user.name@example.com')
      expect(email.getLocalPart()).toBe('user.name')
    })
  })

  describe('equality', () => {
    test('should consider equal emails case-insensitive', () => {
      const email1 = new Email('USER@EXAMPLE.COM')
      const email2 = new Email('user@example.com')
      expect(email1.equals(email2)).toBe(true)
    })

    test('should consider different emails not equal', () => {
      const email1 = new Email('user1@example.com')
      const email2 = new Email('user2@example.com')
      expect(email1.equals(email2)).toBe(false)
    })
  })
})
