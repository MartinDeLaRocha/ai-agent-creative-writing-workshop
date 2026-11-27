package com.example.kosmosconverter

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.LocalDate

class KosmosConverterTest {
    @Test
    fun readmeExample() {
        val r = KosmosConverter.convert(
            LocalDate.of(1974, 6, 17), LocalDate.of(2026, 10, 8))
        assertEquals("04 10 16", r.birth)
        assertEquals("08 01 68", r.interest)
        assertEquals(1, r.periods)
        assertEquals(19106L, r.intervalDays)
    }

    @Test
    fun intervalAndWeekdayPreserved() {
        val birth = LocalDate.of(1980, 3, 5)
        val interest = LocalDate.of(2026, 11, 27)
        val r = KosmosConverter.convert(birth, interest)
        val cb = LocalDate.of(1900 + r.birth.takeLast(2).toInt(),
            r.birth.take(2).toInt(), r.birth.substring(3, 5).toInt())
        val ci = LocalDate.of(1900 + r.interest.takeLast(2).toInt(),
            r.interest.take(2).toInt(), r.interest.substring(3, 5).toInt())
        assertEquals(interest.dayOfWeek, ci.dayOfWeek)
        assertEquals(birth.dayOfWeek, cb.dayOfWeek)
        assertTrue(r.periods > 0)
    }

    @Test(expected = IllegalArgumentException::class)
    fun interestBeforeBirthRejected() {
        KosmosConverter.convert(LocalDate.of(1990, 1, 1), LocalDate.of(1989, 1, 1))
    }
}
