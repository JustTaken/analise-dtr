using CSV
using CairoMakie
using DataFrames
using StatsBase

const Param = Vector{Number}

function testing(x::Vector{<:Number})::Vector{<:Number}
    A = 1000
    B = 0.054
    C = 0.055
    A .* (exp.(.- B .* x) .- exp.(.- C .* x))
end

function load_data(path)
    data = DataFrame(CSV.File(open(path), header=1))

    y = data[!, "Current"]
    l = length(y)

    m = mean(y[l - Int64(round(l / 10)):l])
    y = y .- m
    x = collect(0:l - 1)

    x, y
end

function f(p::Param, x::Vector{<:Number})::Vector{<:Number}
    p[1] .* exp.(.- p[2] .* x) .- p[1] .* exp.(.- p[3] .* x)
end

function data_integral(x::Vector{<:Number}, y::Vector{<:Number})::Number
    let sum = 0
        for i in range(2, length(x))
            sum += (y[i] + y[i - 1]) * (x[i] - x[i - 1]) * 0.5
        end

        sum
    end
end

function rest(y_hat::Vector{<:Number}, y::Vector{<:Number})::Vector{<:Number}
    (y .- y_hat) .^ 2
end

function test_interval(b::Number, c::Number, delta::Number, len::Int64)
    b_vec = collect(range(b - delta, b + delta, length = len))
    c_vec = collect(range(c - delta, c + delta, length = len))

    b_vec, c_vec
end

function find_least(x::Vector{<:Number}, y::Vector{<:Number})
    data = data_integral(x, y)
    base_length::Int64 = 100

    let minimum = 1000, min_b = 0.5, min_c = 0.5, min_a = 1, delta = 0.5
        for r in range(1, 4)
            b, c = test_interval(min_b, min_c, delta, base_length)
            delta = delta / base_length

            for j in range(1, length(b))
                for i in range(1, length(c))
                    a = get_proportion(b[j], c[i], x[1], x[length(x)], data)
                    sse = sum(rest(f(Param([a, b[j], c[i]]), x), y))

                    if sse < minimum
                        minimum = sse
                        min_b = b[j]
                        min_c = c[i]
                        min_a = a
                    end
                end
            end
        end

        minimum, min_a, min_b, min_c
    end
end

function find_fit(x::Vector{<:Number}, y::Vector{<:Number})
    m, A, B, C = find_least(x, y)
    println(m, " ", A, " ", B, " ", C)
    p = Param([A, B, C]) 

    f(p,  x), p
end

function integral(b::Number, c::Number, s::Number, e::Number)::Number
    (exp(-b * s) - exp(-b * e)) / b + (exp(-c * e) - exp(-c * s)) / c
end

function get_proportion(b::Number, c::Number, s::Number, e::Number, data::Number)::Number
    parameterized = integral(b, c, s, e)

    data / parameterized
end

function plot(x::Vector{<:Number}, y::Vector{<:Number}, fit::Vector{<:Number})
    fig = Figure()
    ax = Axis(fig[1, 1], xlabel = "Time", ylabel = "Current", title = "DTR")
    scatter!(ax, x, y, color = :orange)
    scatter!(ax, x, fit, color = :red)

    fig
end

function add_data_to_figure(path, fig, row, col)
    x, y = get_data(path)
    fit, param = find_fit(x, y)
    ax = Axis(fig[row, col])
    scatter!(ax, x, y, color = :orange, markersize=4)
    scatter!(ax, x, fit, color = :red, markersize=4)
end

function plot_all()
    fig = Figure()

    add_data_to_figure("dados1.csv", fig, 1, 1)
    add_data_to_figure("dados2.csv", fig, 1, 2)
    add_data_to_figure("dados3.csv", fig, 2, 1)
    add_data_to_figure("dados4.csv", fig, 2, 2)
    add_data_to_figure("dados5.csv", fig, 3, 1)
    add_data_to_figure("dados6.csv", fig, 3, 2)
    add_data_to_figure("dados7.csv", fig, 4, 1)
    fig
end

# function f(a::Number, b::Number, c::Number, x::Number)::Number
#     a * exp(- b * x) - a * exp( - c * x)
# end

# Partial of the function in relation to A is: exp( - b * x) - exp( - c * x)
# Partial of the function in relation to B is: - a * x * exp( - b * x)
# Partial of the function in relation to C is: a * x * exp( - c * x)
#
# The sum of squared errors is sum((y - y_hat)^2)
# Where y_hat is the choosen functio with current parameters
# And the partial of this function in relation to the parameter P is:
# -2 * sum((y - y_hat) * partial(P))

# Suposelly the function we are trying to ajust is x^2
# using the parameterized function x^a
# So a is 2, but let the code find this out
# Using this coeficient and partially deriving x^a by the variable a
# we have x^a * ln(x). We actually use the sse derivate

# In my understanding, there is no solution to this tyupe of function, so i have to get creative and use some caracteristics
# about the problem and the behaviour of the function
# Like: A is the multiplier of the function, so probably, there is a way to extract it from the calculation and use it in a
# statistics model about the mean of the rest function. If the rest function is biased on a multiple of the parameterized
# function, then probably the parameterized function is just a multiple of our goal function.
# function sse_derivative(p::Param, x::Vector{<:Number}, y::Vector{<:Number})::Vector{Vector{<:Number}}
#     f_values = f(p, x)
#     d_values = derivative(p, x)
# 
#     values::Vector{Vector{Float64}} = []
# 
#     for i in 1:length(p)
#         result::Vector{Float64} = .- 2 .* (y .- f_values) .* d_values[i]
#         push!(values, result)
#     end
# 
#     return values
# end
# 
# function derivative(p::Param, x::Vector{<:Number})::Vector{Vector{<:Number}}
#     [
#         exp.( - p[2] .* x) - exp.(.- p[3] .* x),
#         .- p[1] .* x .* exp.( .- p[2] .* x),
#         p[1] .* x .* exp.( .- p[3] .* x),
#     ] 
# end

# This function is here to test the use case where the behaviour of the data
# is following a x^2 function
# So this function is used in the rest to test the suit case of this especific
# behaviour
# Here b = 1 and c = 2

# The rest function is defined as the sum of squared errors
# where the comparing values is y in this case
# Because the intended usage of this function is the same as privously defined ones
# i'm going to define just for a generic number x and y, and the caller has to
# use the dot notation to broadcast the result into a vector
# function ajust_param_cicle(p::Param, x::Vector{<:Number}, y::Vector{<:Number})::Param
#     div = sse_derivative(p, x, y)
#     rest_sum = sum(rest(f(p, x), y))
# 
#     values = get_new_values(p, div, rest_sum)
#     Param(values)
# end
# 
# function marquat_method(a::Number, div::Number)::Number
#     a - div * 0.01
# end
# 
# function newton_method(a::Number, m::Number, y::Number)::Number
#     a - y / m
# end
# 
# function get_new_value(a::Number, div::Number, r::Number)::Number
#     if abs(div) > 1
#         newton_method(a, div, r)
#     else
#         marquat_method(a, div)
#     end
# end
# 
# function get_new_values(p::Param, div::Vector{<:Number}, r::Number)::Param
#     values::Param = []
# 
#     for i in 1:length(p)
#         append!(values, get_new_value(p[i], div[i], r))
#     end
# 
#     return  values
# end
