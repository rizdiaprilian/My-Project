
-- Covid Death --
Select location, date, population,
total_cases, new_cases, total_deaths, new_deaths
From covid.dbo.[owid-covid-data_death]
order by 1,2;

-- Covid Vaccination --
Select location, date, 
new_tests, total_tests,
new_tests_per_thousand, total_tests_per_thousand
From covid.dbo.[owid-covid-data_vaccination]
order by 1,2;

-- Looking at Total Cases vs Total Deaths
-- Presenting rough estimate on likelihood of death after making contact with Covid
Select location, date, population,
total_cases, total_deaths,
ROUND((total_deaths/total_cases),3) AS ratio_death_cases
From covid.dbo.[owid-covid-data_death]
Where total_deaths is not null and continent is not null
order by 1,2;

-- Looking at Total Cases vs Population
-- Presenting rough estimate on likelihood of death after making contact with Covid
Select location, date, population,
total_cases, ROUND((total_cases/population),3)*100 AS ratio_cases_population
From covid.dbo.[owid-covid-data_death]
Where total_cases is not null And continent is not null
order by 1,2;

-- Finding countries with high infection rate
Select location, population,
Max(total_cases) As HighestInfectionCount, 
Round(MAX(total_cases/population)*100,4) AS ratio_infected_population
From covid.dbo.[owid-covid-data_death]
Where continent is not null
Group by location, population
order by 3 Desc, 4 Desc;

-- Showing Countries with highest death count
Select location, 
Max(cast(total_deaths as int)) As HighestDeathCount
From covid.dbo.[owid-covid-data_death]
Where continent is not null
Group by location
order by 2 Desc;

-- Break the data down by the continent
Select continent, 
Max(cast(total_deaths as int)) As HighestDeathCount
From covid.dbo.[owid-covid-data_death]
Where continent is not null
Group by continent
order by 2 Desc;

-- See daily accumulated new cases in Austria, Germany, United Kingdom (with accumulation till latest date)
SET ANSI_WARNINGS OFF
SELECT CONVERT(VARCHAR(10), date, 110) As date_cleaned, location,
sum(new_cases) As NewCasesCount, sum(cast(new_deaths as int)) As NewDeathCount,
Round(sum(cast(new_deaths as int))/sum(new_cases)*100,4) As RatioDeath
From covid.dbo.[owid-covid-data_death]
Where location in ('United Kingdom', 'Austria', 'Germany') 
Group by date, location
Having sum(new_cases)> 0
Order by location, date;

----
SELECT CONVERT(VARCHAR(10), date, 110) As date_cleaned, location,
sum(new_cases) As NewCasesCount, sum(cast(new_deaths as int)) As NewDeathCount
--sum(cast(new_deaths as int))/sum(new_cases)*100 As RatioDeath
From covid.dbo.[owid-covid-data_death]
Where location in ('United Kingdom', 'Austria', 'Germany') 
Group by location, date
Order by location, date;

-- In Indonesia
SET ANSI_WARNINGS OFF
SELECT CONVERT(VARCHAR(10), date, 110) As date_cleaned, location,
sum(new_cases) As NewCasesCount, sum(cast(new_deaths as int)) As NewDeathCount,
Round(sum(cast(new_deaths as int))/sum(new_cases)*100,4) As RatioDeath
From covid.dbo.[owid-covid-data_death]
Where location in ('Indonesia') 
Group by date, location
Having sum(new_cases)> 0
Order by location, date;

-- Alternative with over partition without Group by clause
Select CONVERT(VARCHAR(10), date, 110) As date_cleaned, location,
sum(new_cases) OVER (PARTITION BY date, location) AS Grandtotal
From covid.dbo.[owid-covid-data_death]
Where location in ('United Kingdom', 'Austria', 'Germany') 
Order by location, date;


-- Looking up Vaccination vs Population After joining death and vaccination
Select dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(Cast(vac.new_vaccinations as bigint)) OVER (PARTITION BY dea.location Order by dea.location, 
dea.date) AS CountVac
From covid.dbo.[owid-covid-data_death] dea
	Join covid.dbo.[owid-covid-data_vaccination] vac
	On dea.iso_code = vac.iso_code And dea.date = vac.date
Where dea.continent is not null and vac.new_vaccinations is not null
Order by 1,2;

-- Using Common Table Expression for Vaccination vs Population

With Population_vs_Vaccination (Location, Date, Population, New_Vaccination, CountVacc)
As
(
Select dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(Cast(vac.new_vaccinations as bigint)) OVER (PARTITION BY dea.location Order by dea.location, 
dea.date) AS CountVac
From covid.dbo.[owid-covid-data_death] dea
	Join covid.dbo.[owid-covid-data_vaccination] vac
	On dea.iso_code = vac.iso_code And dea.date = vac.date
Where dea.continent is not null and vac.new_vaccinations is not null
)
Select Location, CONVERT(VARCHAR(10), Date, 105) As date_cleaned, 
New_Vaccination, CountVacc , Round(CountVacc/Population*100,4) AS  Ratio_Count_Pop
From Population_vs_Vaccination
Where Location IN ('United Kingdom', 'Austria');


-- Temporary Tables
DROP TABLE IF EXISTS #PercentPopulationVaccinated

Create Table #PercentPopulationVaccinated
(
	Location nvarchar(255),
	Date datetime,
	Population numeric, 
	New_vaccinations numeric,
	CountVacc numeric
)

Insert Into #PercentPopulationVaccinated
Select dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(Cast(vac.new_vaccinations as bigint)) OVER (PARTITION BY dea.location Order by dea.location, 
dea.date) AS CountVac
From covid.dbo.[owid-covid-data_death] dea
	Join covid.dbo.[owid-covid-data_vaccination] vac
	On dea.iso_code = vac.iso_code And dea.date = vac.date
Where dea.continent is not null and vac.new_vaccinations is not null

Select Location, CONVERT(VARCHAR(10), Date, 105) As date_cleaned, Population,
New_Vaccinations, CountVacc , Round(CountVacc/Population*100,4) AS  Ratio_Count_Pop
From #PercentPopulationVaccinated
Where Location  = 'Indonesia';

-- Creating View to store data for visualization

Create View PercentPopulationVaccinated_View AS 
Select dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(Cast(vac.new_vaccinations as bigint)) OVER (PARTITION BY dea.location Order by dea.location, 
dea.date) AS CountVac
From covid.dbo.[owid-covid-data_death] dea
	Join covid.dbo.[owid-covid-data_vaccination] vac
	On dea.iso_code = vac.iso_code And dea.date = vac.date
Where dea.continent is not null and vac.new_vaccinations is not null

Select * From PercentPopulationVaccinated_View;