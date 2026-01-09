import { describe, expect, test } from 'bun:test'
import { CPF, ValidationError } from './cpf'

describe('CPF', () => {
  describe('validation', () => {
    test('should accept valid CPF', () => {
      expect(() => new CPF('123.456.789-09')).not.toThrow()
      expect(() => new CPF('12345678909')).not.toThrow()
    })

    test('should reject invalid CPF', () => {
      expect(() => new CPF('123.456.789-00')).toThrow(ValidationError)
      expect(() => new CPF('123.456.789-10')).toThrow(ValidationError)
    })

    test('should reject known invalid sequences', () => {
      expect(() => new CPF('000.000.000-00')).toThrow(ValidationError)
      expect(() => new CPF('111.111.111-11')).toThrow(ValidationError)
      expect(() => new CPF('222.222.222-22')).toThrow(ValidationError)
      expect(() => new CPF('999.999.999-99')).toThrow(ValidationError)
    })

    test('should reject CPF with wrong length', () => {
      expect(() => new CPF('123')).toThrow(ValidationError)
      expect(() => new CPF('12345678901234')).toThrow(ValidationError)
    })

    test('should reject empty CPF', () => {
      expect(() => new CPF('')).toThrow(ValidationError)
    })
  })

  describe('formatting', () => {
    test('should format CPF correctly', () => {
      const cpf = new CPF('12345678909')
      expect(cpf.format()).toBe('123.456.789-09')
    })

    test('should preserve formatting when already formatted', () => {
      const cpf = new CPF('123.456.789-09')
      expect(cpf.format()).toBe('123.456.789-09')
    })
  })

  describe('normalization', () => {
    test('should return raw digits with toString()', () => {
      const cpf = new CPF('123.456.789-09')
      expect(cpf.toString()).toBe('12345678909')
    })

    test('should normalize in JSON serialization', () => {
      const cpf = new CPF('123.456.789-09')
      expect(JSON.stringify({ cpf })).toBe('{"cpf":"12345678909"}')
    })
  })

  describe('equality', () => {
    test('should consider equal CPFs with same value', () => {
      const cpf1 = new CPF('123.456.789-09')
      const cpf2 = new CPF('12345678909')
      expect(cpf1.equals(cpf2)).toBe(true)
    })

    test('should consider different CPFs not equal', () => {
      const cpf1 = new CPF('123.456.789-09')
      const cpf2 = new CPF('987.654.321-00')
      expect(cpf1.equals(cpf2)).toBe(false)
    })
  })
})
