-- CreateEnum
CREATE TYPE "TravelMode" AS ENUM ('DRIVE', 'TRANSIT', 'WALK', 'BICYCLE');

-- CreateEnum
CREATE TYPE "FuelType" AS ENUM ('V93', 'V95', 'V97', 'diesel', 'electrico', 'hibrido', 'gas_licuado');

-- CreateTable
CREATE TABLE "users" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT,
    "google_id" TEXT,
    "avatar_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_preferences" (
    "user_id" TEXT NOT NULL,
    "default_origin_address" TEXT,
    "default_origin_lat" DECIMAL(10,7),
    "default_origin_lng" DECIMAL(10,7),
    "work_days_per_week" INTEGER NOT NULL DEFAULT 5,
    "weeks_per_year" INTEGER NOT NULL DEFAULT 48,
    "fuel_price_margin_pct" DECIMAL(5,2) DEFAULT 5.00,
    "hourly_time_value" DECIMAL(10,2),
    "currency" TEXT NOT NULL DEFAULT 'CLP',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "user_preferences_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "budgets" (
    "id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "source_file" TEXT,
    "processed_at" TIMESTAMP(3),
    "monthly_income" DECIMAL(12,2),
    "monthly_expenses" DECIMAL(12,2),
    "monthly_savings" DECIMAL(12,2),
    "category_breakdown" JSONB,
    "raw_rows" JSONB,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "budgets_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "car_candidates" (
    "id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "source_url" TEXT,
    "source_platform" TEXT,
    "purchase_price" DECIMAL(12,2) NOT NULL,
    "year" INTEGER NOT NULL,
    "fuel_type" "FuelType" NOT NULL,
    "fuel_efficiency_city" DECIMAL(6,2),
    "fuel_efficiency_highway" DECIMAL(6,2),
    "engine_displacement_cc" INTEGER,
    "transmission" TEXT,
    "body_type" TEXT,
    "is_new" BOOLEAN NOT NULL DEFAULT false,
    "tasacion_fiscal" DECIMAL(12,2),
    "permiso_circulacion_yr" DECIMAL(10,2),
    "seguro_anual_estimated" DECIMAL(10,2),
    "mantenimiento_anual_est" DECIMAL(10,2),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "car_candidates_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "commutes" (
    "id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "origin_address" TEXT NOT NULL,
    "origin_lat" DECIMAL(10,7),
    "origin_lng" DECIMAL(10,7),
    "destination_address" TEXT NOT NULL,
    "destination_lat" DECIMAL(10,7),
    "destination_lng" DECIMAL(10,7),
    "frequency_per_week" INTEGER NOT NULL DEFAULT 5,
    "is_required" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "commutes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "route_cache" (
    "id" TEXT NOT NULL,
    "commute_id" TEXT NOT NULL,
    "travel_mode" "TravelMode" NOT NULL,
    "fetched_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "distance_meters" INTEGER NOT NULL,
    "duration_seconds" INTEGER NOT NULL,
    "duration_no_traffic_sec" INTEGER,
    "toll_cost_clp" DECIMAL(10,2) DEFAULT 0,
    "traffic_condition" TEXT,
    "route_polyline" TEXT,
    "raw_response" JSONB,
    "expires_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "route_cache_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "fuel_prices" (
    "id" TEXT NOT NULL,
    "fuel_type" TEXT NOT NULL,
    "region" TEXT,
    "comuna" TEXT,
    "station_name" TEXT,
    "station_address" TEXT,
    "price_per_liter" DECIMAL(8,2) NOT NULL,
    "reported_date" DATE NOT NULL,
    "scraped_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_aggregate" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "fuel_prices_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "tag_tariffs" (
    "id" TEXT NOT NULL,
    "autopista_name" TEXT NOT NULL,
    "tramo_name" TEXT NOT NULL,
    "vehicle_category" TEXT NOT NULL DEFAULT 'liviano',
    "hora_punta" DECIMAL(10,2),
    "hora_valle" DECIMAL(10,2),
    "sabado" DECIMAL(10,2),
    "domingo_festivo" DECIMAL(10,2),
    "effective_from" DATE NOT NULL,
    "effective_until" DATE,
    "source_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "tag_tariffs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "comparisons" (
    "id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "name" TEXT,
    "carCandidateIds" TEXT[],
    "results" JSONB NOT NULL,
    "assumptions" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "comparisons_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE UNIQUE INDEX "users_google_id_key" ON "users"("google_id");

-- CreateIndex
CREATE INDEX "route_cache_commute_id_travel_mode_fetched_at_idx" ON "route_cache"("commute_id", "travel_mode", "fetched_at" DESC);

-- CreateIndex
CREATE UNIQUE INDEX "route_cache_commute_id_travel_mode_fetched_at_key" ON "route_cache"("commute_id", "travel_mode", "fetched_at");

-- CreateIndex
CREATE INDEX "fuel_prices_fuel_type_region_comuna_reported_date_idx" ON "fuel_prices"("fuel_type", "region", "comuna", "reported_date" DESC);

-- CreateIndex
CREATE INDEX "comparisons_user_id_created_at_idx" ON "comparisons"("user_id", "created_at" DESC);

-- AddForeignKey
ALTER TABLE "user_preferences" ADD CONSTRAINT "user_preferences_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "budgets" ADD CONSTRAINT "budgets_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "car_candidates" ADD CONSTRAINT "car_candidates_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "commutes" ADD CONSTRAINT "commutes_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "route_cache" ADD CONSTRAINT "route_cache_commute_id_fkey" FOREIGN KEY ("commute_id") REFERENCES "commutes"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "comparisons" ADD CONSTRAINT "comparisons_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
