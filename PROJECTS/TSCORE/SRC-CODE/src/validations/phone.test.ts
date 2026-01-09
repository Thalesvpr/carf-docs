import { describe, expect, test } from 'bun:test'
import { Phone } from './phone'
import { ValidationError } from './cpf'

describe('Phone', () => {
  describe('validation', () => {
    test('should accept valid mobile phones (11 digits)', () => {
      expect(() => new Phone('(11) 98765-4321')).not.toThrow()
      expect(() => new Phone('11987654321')).not.toThrow()
      expect(() => new Phone('(21) 99876-5432')).not.toThrow()
    })

    test('should accept valid landline phones (10 digits)', () => {
      expect(() => new Phone('(11) 3456-7890')).not.toThrow()
      expect(() => new Phone('1134567890')).not.toThrow()
      expect(() => new Phone('(21) 2345-6789')).not.toThrow()
    })

    test('should reject mobile without 9 prefix', () => {
      expect(() => new Phone('(11) 88765-4321')).toThrow(ValidationError)
      expect(() => new Phone('11887654321')).toThrow(ValidationError)
    })

    test('should reject invalid DDD', () => {
      expect(() => new Phone('(00) 98765-4321')).toThrow(ValidationError)
      expect(() => new Phone('(10) 98765-4321')).toThrow(ValidationError)
    })

    test('should reject phones with wrong length', () => {
      expect(() => new Phone('123')).toThrow(ValidationError)
      expect(() => new Phone('123456789012')).toThrow(ValidationError)
    })

    test('should reject empty phone', () => {
      expect(() => new Phone('')).toThrow(ValidationError)
    })
  })

  describe('formatting', () => {
    test('should format mobile phone correctly', () => {
      const phone = new Phone('11987654321')
      expect(phone.format()).toBe('(11) 98765-4321')
    })

    test('should format landline phone correctly', () => {
      const phone = new Phone('1134567890')
      expect(phone.format()).toBe('(11) 3456-7890')
    })

    test('should preserve formatting when already formatted', () => {
      const mobile = new Phone('(11) 98765-4321')
      expect(mobile.format()).toBe('(11) 98765-4321')

      const landline = new Phone('(11) 3456-7890')
      expect(landline.format()).toBe('(11) 3456-7890')
    })
  })

  describe('normalization', () => {
    test('should return raw digits with toString()', () => {
      const phone = new Phone('(11) 98765-4321')
      expect(phone.toString()).toBe('11987654321')
    })

    test('should normalize in JSON serialization', () => {
      const phone = new Phone('(11) 98765-4321')
      expect(JSON.stringify({ phone })).toBe('{"phone":"11987654321"}')
    })
  })

  describe('parts extraction', () => {
    test('should extract DDD correctly', () => {
      const phone = new Phone('(11) 98765-4321')
      expect(phone.getDDD()).toBe('11')
    })

    test('should extract number without DDD correctly', () => {
      const mobile = new Phone('(11) 98765-4321')
      expect(mobile.getNumber()).toBe('987654321')

      const landline = new Phone('(11) 3456-7890')
      expect(landline.getNumber()).toBe('34567890')
    })
  })

  describe('type checking', () => {
    test('should identify mobile phones', () => {
      const mobile = new Phone('(11) 98765-4321')
      expect(mobile.isMobile()).toBe(true)
      expect(mobile.isLandline()).toBe(false)
    })

    test('should identify landline phones', () => {
      const landline = new Phone('(11) 3456-7890')
      expect(landline.isMobile()).toBe(false)
      expect(landline.isLandline()).toBe(true)
    })
  })

  describe('equality', () => {
    test('should consider equal phones with same value', () => {
      const phone1 = new Phone('(11) 98765-4321')
      const phone2 = new Phone('11987654321')
      expect(phone1.equals(phone2)).toBe(true)
    })

    test('should consider different phones not equal', () => {
      const phone1 = new Phone('(11) 98765-4321')
      const phone2 = new Phone('(11) 98765-4322')
      expect(phone1.equals(phone2)).toBe(false)
    })
  })
})
