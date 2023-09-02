import {expect, test} from 'vitest'
import {validateType, validateUUID} from '@/util/qrcode-util'

test('validateType', () => {
  test("accepts a person", () => {
    expect(validateType('P')).toBe(true)
  })

  test("accepts an item", () => {
    expect(validateType('P')).toBe(true)
  })

  test("rejects other types", () => {
    expect(validateType('Z')).toBe(false)
  })
})

test('validateUUID', () => {
  test("accepts a valid UUID", () => {
    expect(validateUUID('884b224b-6aa5-4949-855d-95e72d1e3a1c')).toBe(true)
  })

  test("rejects an invalid UUID", () => {
    expect(validateType('884b224b-6aa5-f949-855d-95e72d1e3a1c')).toBe(false)
  })
})
